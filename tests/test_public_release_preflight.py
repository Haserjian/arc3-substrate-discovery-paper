from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "tools" / "paper" / "build_public_release_preflight.py"


def test_public_release_preflight_builder_runs_without_publish_or_submit(tmp_path):
    output_dir = _build_preflight(tmp_path)
    report = _read_json(output_dir / "readiness_report.json")

    assert report["kind"] == "public_release_preflight_readiness_report"
    assert report["github_publish_authorization_required"] is True
    assert report["no_github_repo_published"] is True
    assert report["no_kaggle_submission_made"] is True
    assert report["no_paper_submission_made"] is True
    assert report["no_official_arc_run_invoked"] is True
    assert report["no_new_capability_claim_made"] is True


def test_publish_record_flag_updates_github_action_fields(tmp_path):
    output_dir = _build_preflight(tmp_path, github_publish_recorded=True)
    report = _read_json(output_dir / "readiness_report.json")

    assert report["github_publish_authorization_required"] is False
    assert report["no_github_repo_published"] is False
    assert report["no_kaggle_submission_made"] is True
    assert report["no_paper_submission_made"] is True
    assert report["no_official_arc_run_invoked"] is True
    assert report["no_new_capability_claim_made"] is True


def test_readiness_report_schema_and_blocks_unverified_public_urls(tmp_path):
    output_dir = _build_preflight(tmp_path)
    report = _read_json(output_dir / "readiness_report.json")

    assert report["public_release_ready"] is False
    assert report["proposed_public_repo_name"] == "arc3-substrate-discovery-paper"
    assert report["proposed_public_repo_url"] == (
        "https://github.com/Haserjian/arc3-substrate-discovery-paper"
    )
    assert "proposed_public_repo_url_not_published_or_not_public" in report["blocking_issues"]
    assert "kaggle_public_url_not_verified" in report["blocking_issues"]
    assert "release_candidate_link_scan_failed" not in report["blocking_issues"]
    assert report["paper_url_update_pending"] is False


def test_release_candidate_has_required_top_level_files(tmp_path):
    output_dir = _build_preflight(tmp_path)
    release = output_dir / "release_candidate"

    for name in ["README.md", "LICENSE", "NOTICE", "THIRD_PARTY_LICENSES.md"]:
        assert (release / name).exists(), name

    readme = (release / "README.md").read_text()
    assert "Release Package" in readme
    assert "has not been published" not in readme
    assert "No private-eval capability claim" in readme
    assert "No general ARC-AGI-3 solver claim" in readme
    assert "No autonomous substrate discovery claim" in readme


def test_release_inventory_covers_every_candidate_file(tmp_path):
    output_dir = _build_preflight(tmp_path)
    release = output_dir / "release_candidate"
    inventory = _read_json(output_dir / "release_file_inventory.json")

    release_files = {
        str(path.relative_to(release))
        for path in release.rglob("*")
        if path.is_file()
    }
    inventory_files = {item["release_path"] for item in inventory["included_files"]}

    assert release_files == inventory_files
    assert inventory["summary"]["release_file_count"] == len(release_files)


def test_release_candidate_scans_have_no_local_paths_secrets_or_forbidden_claims(tmp_path):
    output_dir = _build_preflight(tmp_path)
    scan = _read_json(output_dir / "release_scan_report.json")

    assert scan["secrets_scan_status"] == "pass"
    assert scan["local_path_scan_status"] == "pass"
    assert scan["forbidden_claim_scan_status"] == "pass"
    assert scan["stale_score_terminology_status"] == "pass"
    assert scan["link_scan_status"] == "pass"
    assert scan["secret_hits"] == []
    assert scan["local_path_hits"] == []
    assert scan["forbidden_claim_hits"] == []
    assert scan["stale_score_hits"] == []
    assert scan["link_scan"]["metadata_repo_url"] == (
        "https://github.com/Haserjian/arc3-substrate-discovery-paper"
    )
    assert scan["link_scan"]["pdf_text_status"] == "checked"
    assert scan["link_scan"]["stale_private_repo_url_hits"] == []


def test_notebook_manifest_release_copy_is_sanitized(tmp_path):
    output_dir = _build_preflight(tmp_path)
    manifest = _read_json(
        output_dir
        / "release_candidate"
        / "kaggle"
        / "notebook_candidate"
        / "notebook_candidate_manifest.json"
    )

    assert manifest["release_manifest_sanitized"] is True
    assert manifest["agent_path"] == "kaggle/notebook_candidate/my_agent.py"
    assert "/Users/" not in json.dumps(manifest)


def test_evidence_path_audit_has_no_missing_paths(tmp_path):
    output_dir = _build_preflight(tmp_path)
    audit = _read_json(output_dir / "evidence_path_audit.json")

    assert audit["evidence_path_status"] == "pass"
    assert audit["missing_count"] == 0
    assert audit["missing_paths"] == []
    assert audit["intentionally_excluded_count"] == 1


def test_license_audit_has_required_release_posture(tmp_path):
    output_dir = _build_preflight(tmp_path)
    audit = _read_json(output_dir / "license_audit.json")

    assert audit["recommended_submitter_license"] in {"MIT-0", "CC0"}
    assert audit["whether_root_private_repo_license_needs_to_change"] == "no"
    assert audit["whether_release_candidate_package_level_license_is_sufficient"] == "yes"
    assert audit["unknown_license_blockers"] == []
    assert "not legal advice" in audit["cautious_language"]


def test_license_audit_covers_kaggle_notebook_imports(tmp_path):
    output_dir = _build_preflight(tmp_path)
    audit = _read_json(output_dir / "license_audit.json")
    imports = audit["kaggle_notebook_import_inventory"]
    runtime = {item["module_or_package"] for item in imports["runtime_third_party"]}

    assert {"arc-agi", "arcengine", "agents", "python-dotenv", "pandas"} <= runtime
    assert all(item["redistributed_in_release_candidate"] is False for item in imports["runtime_third_party"])
    assert "competition-provided arc runtime code is referenced, not vendored" in imports["coverage_note"].lower()


def test_kaggle_status_check_uses_existing_record_without_new_submission(tmp_path):
    output_dir = _build_preflight(tmp_path)
    status = _read_json(output_dir / "kaggle_status_check.json")

    assert status["kaggle_submission_exists"] is True
    assert status["accepted_or_succeeded"] is True
    assert str(status["score_observed"]) == "0.0"
    assert status["no_new_submission_made"] is True
    assert status["public_access_verified"] is False


def _build_preflight(tmp_path: Path, *, github_publish_recorded: bool = False) -> Path:
    output_dir = tmp_path / "public_release_preflight"
    cmd = [
        sys.executable,
        str(BUILDER),
        "--output-dir",
        str(output_dir),
        "--skip-network",
        "--skip-docs",
    ]
    if github_publish_recorded:
        cmd.append("--github-publish-recorded")
    subprocess.run(
        cmd,
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return output_dir


def _read_json(path: Path):
    return json.loads(path.read_text())
