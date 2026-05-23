from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "docs" / "paper"
SOURCE = PAPER / "manuscript_v1.md"
READER = PAPER / "submission_manuscript.md"
PDF = PAPER / "submission_candidate.pdf"
METADATA = PAPER / "submission_candidate_metadata.json"
BUILDER = ROOT / "tools" / "paper" / "build_submission_candidate.py"

REQUIRED_REFERENCE_KEYS = {
    "ARCPrize2026Paper",
    "ARCAGI3Methodology",
    "ARCAGI3Track",
    "ARCAGI3Benchmark2026",
    "Rodionov2026EWM",
    "RudakovEtAl2025Graph",
    "LiuEtAl2026MAP",
}
INTERNAL_FRONTMATTER_FLAGS = {
    "paper_status:",
    "submitted:",
    "peer_reviewed:",
    "kaggle_score:",
    "kaggle_submission_status:",
    "linked_kaggle_score:",
    "accuracy_claim_status:",
    "public_scorecard_evidence:",
    "licensing_target:",
    "last_checked:",
}


def test_submission_candidate_builder_runs_from_repo_environment_without_mutating_candidate(tmp_path):
    before = {path: _sha256(path) for path in [READER, PDF, METADATA]}

    result = subprocess.run(
        [sys.executable, str(BUILDER), "--output-dir", str(tmp_path)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    assert result.stderr == ""
    assert {path: _sha256(path) for path in [READER, PDF, METADATA]} == before

    generated_reader = tmp_path / "submission_manuscript.md"
    generated_pdf = tmp_path / "submission_candidate.pdf"
    generated_metadata = tmp_path / "submission_candidate_metadata.json"
    assert generated_reader.exists()
    assert generated_pdf.exists()
    assert generated_metadata.exists()

    metadata = json.loads(generated_metadata.read_text())
    assert metadata["checks"]["pdf_generated_nonempty"] is True
    assert metadata["checks"]["reader_markdown_has_no_absolute_users_paths"] is True
    assert metadata["checks"]["reader_markdown_has_no_internal_frontmatter_flags"] is True
    assert metadata["checks"]["source_manuscript_preserved"] is True
    assert metadata["toolchain"]["reportlab"] is not None
    assert metadata["toolchain"]["pypdf"] is not None


def test_checked_in_candidate_matches_normalized_rebuild(tmp_path):
    subprocess.run(
        [sys.executable, str(BUILDER), "--output-dir", str(tmp_path)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    rebuilt_reader = tmp_path / "submission_manuscript.md"
    rebuilt_pdf = tmp_path / "submission_candidate.pdf"
    rebuilt_metadata = json.loads((tmp_path / "submission_candidate_metadata.json").read_text())

    assert rebuilt_reader.read_text() == READER.read_text()
    assert _pdf_text(rebuilt_pdf) == _pdf_text(PDF)

    current_metadata = _metadata()
    for key in [
        "checks",
        "citation_keys",
        "claim_id_handling",
        "page_count",
        "provenance_handling",
        "repo_relative_paths_collected",
        "source_manuscript",
        "source_sha256",
        "used_claim_ids",
    ]:
        assert rebuilt_metadata[key] == current_metadata[key]


def test_submission_candidate_files_exist_and_pdf_is_nonempty():
    assert READER.exists()
    assert PDF.exists()
    assert METADATA.exists()
    assert PDF.stat().st_size > 10_000

    metadata = _metadata()
    assert metadata["pdf_path"] == "docs/paper/submission_candidate.pdf"
    assert metadata["reader_markdown"] == "docs/paper/submission_manuscript.md"
    assert metadata["page_count"] > 0
    assert metadata["checks"]["pdf_generated_nonempty"] is True


def test_reader_markdown_strips_internal_flags_and_local_paths():
    text = READER.read_text()

    assert "/Users/" not in text
    for flag in INTERNAL_FRONTMATTER_FLAGS:
        assert flag not in text
    assert not text.startswith("---")
    assert "This is manuscript v1" not in text
    assert "Prior work still needs final citation-style polish" not in text

    metadata = _metadata()
    assert metadata["checks"]["reader_markdown_has_no_absolute_users_paths"] is True
    assert metadata["checks"]["reader_markdown_has_no_internal_frontmatter_flags"] is True


def test_source_manuscript_remains_draft_source_of_truth():
    source = SOURCE.read_text()

    for flag in [
        "paper_status: draft",
        "submitted: false",
        "peer_reviewed: false",
        "kaggle_submission_status: submitted_succeeded",
        "linked_kaggle_score: 0.0",
    ]:
        assert flag in source
    assert _metadata()["source_sha256"] == _sha256(SOURCE)
    assert _metadata()["checks"]["source_manuscript_preserved"] is True


def test_required_reader_sections_are_present():
    text = READER.read_text()

    for heading in [
        "# Failure-Driven Substrate Discovery for ARC-AGI-3",
        "## Abstract",
        "## Claim Boundary",
        "## Introduction",
        "## Related Work",
        "## Method: Failure-Driven Substrate Discovery",
        "### Source-Informed Evidence Boundary",
        "## System Architecture / Receipt Discipline",
        "## Cross-Game Results",
        "## Limitations",
        "## Conclusion",
        "## Data and Reproducibility Availability",
        "## Appendix A: Claim Inventory Summary",
        "## References",
    ]:
        assert heading in text


def test_citations_resolve_bidirectionally_in_reader_markdown():
    text = READER.read_text()
    body = text.split("## References", 1)[0]
    citation_keys = _citation_keys(body)
    reference_keys = set(re.findall(r"^- \[([A-Za-z0-9]+)\]", text, flags=re.MULTILINE))

    assert citation_keys == REQUIRED_REFERENCE_KEYS
    assert reference_keys == REQUIRED_REFERENCE_KEYS
    assert _metadata()["checks"]["required_reference_keys_present"] is True


def test_claim_ids_are_presented_through_appendix_not_raw_artifact_parentheticals():
    text = READER.read_text()
    body = text.split("## Data and Reproducibility Availability", 1)[0]

    assert "(App. A, C22)" in body
    assert "(App. A, C36, C37)" in body
    assert "## Appendix A: Claim Inventory Summary" in text
    assert "| C39 | OBSERVED |" in text

    raw_repo_paths_before_repro = re.findall(
        r"`((?:artifacts|docs|tests|kaggle|object_substrate_v0|planner_v0|agents)/[^`]+)`",
        body,
    )
    assert raw_repo_paths_before_repro == []

    metadata = _metadata()
    assert metadata["claim_id_handling"] == "in_body_refs_converted_to_appendix_a_claim_index"
    assert metadata["provenance_handling"] == (
        "repo_relative_paths_collected_in_data_and_reproducibility_availability"
    )


def test_reproducibility_section_contains_repo_links_and_evidence_paths():
    text = READER.read_text()

    assert "https://github.com/Haserjian/arc3-substrate-discovery-paper" in text
    assert "https://github.com/Haserjian/arc3_agent" not in text
    assert "https://www.kaggle.com/code/timhaserjian/arc3-object-substrate-submission-candidate" in text
    for path in [
        "artifacts/kaggle_submission_preflight/kaggle_submission_record/submission_record.json",
        "artifacts/object_substrate_v0/run_005_object_aware_wall_fix/receipt.json",
        "artifacts/object_substrate_v0/tr87_run_001_object_aware/receipt.json",
        "artifacts/object_substrate_v0/gamma3a_third_game_substrate_audit/transferability_map_vs_ls20_tr87.json",
    ]:
        assert path in text


def test_non_claim_boundaries_are_preserved_in_reader_candidate():
    text = READER.read_text()

    required_phrases = [
        "linked Kaggle submission with Kaggle public score `0.0`",
        "not a general ARC-AGI-3 agent",
        "not a claim of autonomous",
        "human-in-the-loop failure-analysis",
        "identified public-game substrates",
        "public-scorecard score",
        "This is not a high-score leaderboard paper",
        "not evidence of private-eval generality",
        "no official run, no planner, no capability claim",
        "Interaction-derived?",
        "Kaggle linkage",
        "Automation boundary",
        "Threat model",
        "Algorithm 1: Failure-Driven Substrate Discovery",
        "game instance `g`",
    ]
    for phrase in required_phrases:
        assert phrase in text

    forbidden = [
        "submitted: true",
        "peer_reviewed: true",
        "private-eval capability demonstrated",
        "general ARC-AGI-3 solution",
        "solves ARC-AGI-3",
        "discovered public-game substrates",
        "public score `3.57`",
        "public score `4.76`",
        "predeclared gate",
        "generalized across public ontology types",
        "development discipline for discovering the substrate",
        "| Boundary |",
        "linked public score `0.0`",
    ]
    for phrase in forbidden:
        assert phrase not in text

    assert _metadata()["checks"]["non_claims_preserved"] is True


def test_reader_candidate_has_no_known_generated_prose_nits():
    text = READER.read_text()

    assert "Manuscript v1 treats" not in text
    assert "the object-substrate claim range cover " not in text
    assert "the object-substrate claim range covers" not in text
    assert "main safety rail for object-substrate and cross-game evidence" in text
    assert "Reader summaries may shorten long machine identifiers" in text


def test_appendix_reader_summaries_avoid_unnecessary_long_machine_identifiers():
    appendix = READER.read_text().split("## Appendix A: Claim Inventory Summary", 1)[1]
    appendix = appendix.split("## References", 1)[0]

    for phrase in [
        "method_transfers_ontology_doesnt",
        "bsqsshqpox_sequence_rule_validation",
        "selector_position_change",
        "sequence_state_change",
        "ready_for_gamma2d_planner",
        "prediction_mismatch_count",
    ]:
        assert phrase not in appendix
    assert "method-transfers/ontology-does-not-transfer finding" in appendix
    assert "source-specific sequence-rule validation predicate" in appendix


def test_pdf_text_has_no_inline_numeric_spacing_artifacts():
    text = _pdf_text(PDF)

    for phrase in [
        "0 . 0",
        "3 . 57",
        "4 . 76",
        "4 / 20",
        "20 / 20",
        "80 / 80",
        "81 / 81",
    ]:
        assert phrase not in text


def _citation_keys(text: str) -> set[str]:
    keys: set[str] = set()
    for marker in re.findall(r"\[@([^\]]+)\]", text):
        keys.update(part.strip().lstrip("@") for part in marker.split(";"))
    return keys


def _metadata() -> dict:
    return json.loads(METADATA.read_text())


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def _pdf_text(path: Path) -> str:
    return "\n".join((page.extract_text() or "") for page in PdfReader(str(path)).pages)
