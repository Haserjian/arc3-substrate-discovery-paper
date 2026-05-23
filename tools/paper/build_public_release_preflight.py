from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import shutil
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
PREFLIGHT = ROOT / "artifacts" / "public_release_preflight"
RELEASE_DIR_NAME = "release_candidate"
DOCS_PAPER = ROOT / "docs" / "paper"
PROPOSED_REPO_NAME = "arc3-substrate-discovery-paper"
PROPOSED_REPO_URL = f"https://github.com/Haserjian/{PROPOSED_REPO_NAME}"
CURRENT_PRIVATE_REPO_NAME = "".join(("arc3", "_agent"))
CURRENT_PRIVATE_REPO_URL = f"https://github.com/Haserjian/{CURRENT_PRIVATE_REPO_NAME}"
KAGGLE_NOTEBOOK_URL = (
    "https://www.kaggle.com/code/timhaserjian/"
    "arc3-object-substrate-submission-candidate"
)

RULE_SOURCE_URLS = {
    "paper_prize": "https://arcprize.org/competitions/2026/paper",
    "arc_prize_2026": "https://arcprize.org/competitions/2026",
    "arc_agi_3_track": "https://arcprize.org/competitions/2026/arc-agi-3",
    "scoring_methodology": "https://docs.arcprize.org/methodology",
}

REQUIRED_RELEASE_ROOT_FILES = {
    "README.md",
    "LICENSE",
    "NOTICE",
    "THIRD_PARTY_LICENSES.md",
}

EXCLUDED_NAMES = {
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".DS_Store",
}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}

SECRET_PATTERNS = {
    "aws_access_key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "github_token": re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    "openai_key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "kaggle_key_assignment": re.compile(r"\bKAGGLE_KEY\s*="),
    "openai_key_assignment": re.compile(r"\bOPENAI_API_KEY\s*="),
}

LOCAL_PATH_PATTERNS = {
    "users_path": "/" + "Users/",
    "mnt_data_path": "/mnt/" + "data/",
    "localhost_assumption": "localhost",
}

STALE_SCORE_PATTERNS = [
    "linked public score",
    "public score `3.57`",
    "public score `4.76`",
    "public score 3.57",
    "public score 4.76",
]

FORBIDDEN_CLAIM_PATTERNS = [
    "private-eval capability demonstrated",
    "private eval capability demonstrated",
    "general ARC-AGI-3 solution",
    "solves ARC-AGI-3",
    "positive Kaggle capability",
    "positive Kaggle leaderboard capability",
    "autonomous substrate discovery system",
]

NEGATING_WORDS = (
    "not",
    "no ",
    "does not",
    "do not",
    "refute",
    "refutes",
    "refuted",
    "without",
)


@dataclass(frozen=True)
class ReleaseItem:
    source_path: str
    release_path: str
    role: str
    origin: str
    license_treatment: str
    reason_included: str
    sanitized: bool = False


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PREFLIGHT,
        help="Directory for release preflight artifacts.",
    )
    parser.add_argument(
        "--skip-network",
        action="store_true",
        help="Skip unauthenticated URL checks for deterministic tests.",
    )
    parser.add_argument(
        "--skip-docs",
        action="store_true",
        help="Do not write docs/paper/public_release_plan.md.",
    )
    parser.add_argument(
        "--browser-kaggle-inspected",
        action="store_true",
        help="Record that a signed-in browser Kaggle status check was performed.",
    )
    parser.add_argument("--browser-kaggle-status", default=None)
    parser.add_argument("--browser-kaggle-score", default=None)
    parser.add_argument("--browser-kaggle-notebook-visibility", default=None)
    parser.add_argument(
        "--github-publish-recorded",
        action="store_true",
        help="Record that the fresh public GitHub repository has been published.",
    )
    args = parser.parse_args()

    generated_at = datetime.now(timezone.utc).isoformat()
    output_dir = resolve_output_dir(args.output_dir)
    release_dir = output_dir / RELEASE_DIR_NAME
    reset_dir(output_dir)
    release_dir.mkdir(parents=True, exist_ok=True)

    inventory = build_release_candidate(output_dir, release_dir, generated_at)
    write_json(output_dir / "release_file_inventory.json", inventory)

    kaggle_status = build_kaggle_status_check(
        generated_at=generated_at,
        skip_network=args.skip_network,
        browser_inspected=args.browser_kaggle_inspected,
        browser_status=args.browser_kaggle_status,
        browser_score=args.browser_kaggle_score,
        browser_notebook_visibility=args.browser_kaggle_notebook_visibility,
    )
    write_json(output_dir / "kaggle_status_check.json", kaggle_status)

    rule_snapshot = build_rule_snapshot(
        generated_at=generated_at,
        skip_network=args.skip_network,
    )
    write_json(output_dir / "rule_snapshot.json", rule_snapshot)

    license_audit = build_license_audit(generated_at, inventory)
    write_json(output_dir / "license_audit.json", license_audit)

    scan_report = build_scan_report(generated_at, release_dir)
    write_json(output_dir / "release_scan_report.json", scan_report)

    evidence_audit = build_evidence_path_audit(generated_at, inventory)
    write_json(output_dir / "evidence_path_audit.json", evidence_audit)

    readiness = build_readiness_report(
        generated_at=generated_at,
        output_dir=output_dir,
        inventory=inventory,
        kaggle_status=kaggle_status,
        rule_snapshot=rule_snapshot,
        license_audit=license_audit,
        scan_report=scan_report,
        evidence_audit=evidence_audit,
        skip_network=args.skip_network,
        github_publish_recorded=args.github_publish_recorded,
    )
    write_json(output_dir / "readiness_report.json", readiness)

    trajectory = build_trajectory_record(generated_at, output_dir, readiness)
    write_json(output_dir / "trajectory_record.json", trajectory)

    if not args.skip_docs:
        plan = build_public_release_plan(readiness, license_audit, evidence_audit)
        (DOCS_PAPER / "public_release_plan.md").write_text(plan)


def resolve_output_dir(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def reset_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def build_release_candidate(
    output_dir: Path,
    release_dir: Path,
    generated_at: str,
) -> dict[str, Any]:
    items: list[ReleaseItem] = []

    add_generated_release_files(items, release_dir, generated_at)

    add_file(
        items,
        "artifacts/kaggle_submission_preflight/package_candidate/LICENSE",
        "LICENSE",
        "release license",
        "submitter_authored",
        "MIT-0",
        "Package-level permissive license for submitter-authored release contents.",
    )
    add_file(
        items,
        "artifacts/kaggle_submission_preflight/package_candidate/NOTICE",
        "NOTICE",
        "release notice",
        "submitter_authored",
        "MIT-0",
        "Discloses package scope and source-informed constants.",
    )
    add_file(
        items,
        "artifacts/kaggle_submission_preflight/package_candidate/THIRD_PARTY_LICENSES.md",
        "THIRD_PARTY_LICENSES.md",
        "third-party license inventory",
        "submitter_authored",
        "MIT-0",
        "States third-party runtime posture for the release candidate.",
    )

    paper_files = [
        "docs/paper/submission_candidate.pdf",
        "docs/paper/submission_manuscript.md",
        "docs/paper/claim_inventory.md",
        "docs/paper/references.md",
        "docs/paper/results_table.md",
        "docs/paper/known_gaps.md",
        "docs/paper/cross_game_substrate_results.md",
        "docs/paper/substrate_gap_taxonomy.md",
        "docs/paper/submission_candidate_metadata.json",
    ]
    for source in paper_files:
        add_file(
            items,
            source,
            f"paper/{Path(source).name}",
            "paper evidence and reader artifact",
            "submitter_authored",
            "MIT-0",
            "Supports the paper claim boundary and reader-facing reproducibility package.",
        )

    kaggle_package_files = [
        path
        for path in sorted((ROOT / "artifacts/kaggle_submission_preflight/package_candidate").iterdir())
        if path.is_file() and path.name not in {"LICENSE", "NOTICE", "THIRD_PARTY_LICENSES.md"}
    ]
    for path in kaggle_package_files:
        add_file(
            items,
            rel(path),
            f"kaggle/package_candidate/{path.name}",
            "Kaggle package surface",
            "submitter_authored",
            "MIT-0",
            "Preserves the linked Kaggle package candidate surface without private history.",
        )

    notebook_files = [
        "artifacts/kaggle_submission_preflight/kaggle_notebook_candidate/arc3_object_substrate_submission.ipynb",
        "artifacts/kaggle_submission_preflight/kaggle_notebook_candidate/my_agent.py",
    ]
    for source in notebook_files:
        add_file(
            items,
            source,
            f"kaggle/notebook_candidate/{Path(source).name}",
            "Kaggle notebook candidate",
            "submitter_authored",
            "MIT-0",
            "Preserves the notebook/agent surface tied to the submission record.",
        )
    add_sanitized_json(
        items,
        "artifacts/kaggle_submission_preflight/kaggle_notebook_candidate/notebook_candidate_manifest.json",
        "kaggle/notebook_candidate/notebook_candidate_manifest.json",
        sanitize_notebook_manifest,
        "Kaggle notebook candidate manifest",
        "submitter_authored",
        "MIT-0",
        "Rewrites absolute local paths into release-relative paths for public sharing.",
    )

    submission_record_files = [
        "artifacts/kaggle_submission_preflight/kaggle_submission_record/submission_record.json",
        "artifacts/kaggle_submission_preflight/kaggle_submission_record/notebook_version_commit_record.json",
        "artifacts/kaggle_submission_preflight/kaggle_submission_record/notebook_pre_submission_snapshot.json",
        "artifacts/kaggle_submission_preflight/kaggle_submission_record/post_submission_agent_review.json",
        "artifacts/kaggle_submission_preflight/kaggle_submission_record/pre_submission_snapshot.json",
    ]
    for source in submission_record_files:
        add_file(
            items,
            source,
            f"kaggle/submission_record/{Path(source).name}",
            "Kaggle submission linkage evidence",
            "generated",
            "MIT-0",
            "Supports the linked Kaggle status and 0.0 score boundary.",
        )

    for source in key_evidence_paths():
        add_file(
            items,
            source,
            source,
            "paper-cited evidence receipt",
            "generated",
            "MIT-0",
            "Evidence path cited by the paper candidate or required by the release audit.",
        )

    add_file(
        items,
        "tools/paper/build_submission_candidate.py",
        "tools/paper/build_submission_candidate.py",
        "paper build script",
        "submitter_authored",
        "MIT-0",
        "Allows regeneration of the reader-clean paper candidate.",
    )
    add_file(
        items,
        "tools/paper/build_public_release_preflight.py",
        "tools/paper/build_public_release_preflight.py",
        "release preflight script",
        "submitter_authored",
        "MIT-0",
        "Documents how this release candidate was assembled and scanned.",
    )
    add_file(
        items,
        "tests/test_paper_submission_candidate.py",
        "tests/test_paper_submission_candidate.py",
        "paper artifact guard tests",
        "submitter_authored",
        "MIT-0",
        "Guards reproducible PDF generation and paper claim boundaries.",
    )
    if (ROOT / "tests/test_public_release_preflight.py").exists():
        add_file(
            items,
            "tests/test_public_release_preflight.py",
            "tests/test_public_release_preflight.py",
            "release preflight guard tests",
            "submitter_authored",
            "MIT-0",
            "Guards the local public-release package preflight.",
        )
    add_file(
        items,
        "pyproject.toml",
        "pyproject.toml",
        "minimal project metadata",
        "submitter_authored",
        "MIT-0",
        "Documents optional paper/test dependencies used for reproducibility checks.",
    )
    if (ROOT / "uv.lock").exists():
        add_file(
            items,
            "uv.lock",
            "uv.lock",
            "dependency lockfile",
            "generated",
            "MIT-0",
            "Pins the local dependency resolution used by tests and paper tooling.",
        )

    copy_items(items, release_dir)

    inventory = {
        "kind": "public_release_file_inventory",
        "schema_version": "v0",
        "generated_at": generated_at,
        "release_directory": rel(release_dir),
        "included_files": [item.__dict__ for item in items],
        "excluded_files": excluded_file_records(),
        "summary": {
            "included_file_count": len(items),
            "release_file_count": sum(1 for path in release_dir.rglob("*") if path.is_file()),
            "proposed_public_repo_name": PROPOSED_REPO_NAME,
            "proposed_public_repo_url": PROPOSED_REPO_URL,
        },
    }
    return inventory


def add_generated_release_files(
    items: list[ReleaseItem],
    release_dir: Path,
    generated_at: str,
) -> None:
    readme = release_readme(generated_at)
    (release_dir / "README.md").write_text(readme)
    items.append(
        ReleaseItem(
            source_path="<generated>",
            release_path="README.md",
            role="release overview and reproducibility instructions",
            origin="submitter_authored",
            license_treatment="MIT-0",
            reason_included="Explains scope, reproduction steps, claim boundaries, and non-actions.",
        )
    )


def add_file(
    items: list[ReleaseItem],
    source_path: str,
    release_path: str,
    role: str,
    origin: str,
    license_treatment: str,
    reason_included: str,
) -> None:
    source = ROOT / source_path
    if not source.exists():
        items.append(
            ReleaseItem(
                source_path=source_path,
                release_path=release_path,
                role=role,
                origin=origin,
                license_treatment="blocker_unknown",
                reason_included=f"Missing source file intended for release: {reason_included}",
            )
        )
        return
    if should_exclude(source):
        return
    items.append(
        ReleaseItem(
            source_path=source_path,
            release_path=release_path,
            role=role,
            origin=origin,
            license_treatment=license_treatment,
            reason_included=reason_included,
        )
    )


def add_sanitized_json(
    items: list[ReleaseItem],
    source_path: str,
    release_path: str,
    sanitizer: Any,
    role: str,
    origin: str,
    license_treatment: str,
    reason_included: str,
) -> None:
    source = ROOT / source_path
    if not source.exists():
        add_file(
            items,
            source_path,
            release_path,
            role,
            origin,
            "blocker_unknown",
            reason_included,
        )
        return
    data = json.loads(source.read_text())
    sanitized = sanitizer(data)
    target = PREFLIGHT / "_sanitized" / release_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(sanitized, indent=2, sort_keys=True) + "\n")
    items.append(
        ReleaseItem(
            source_path=source_path,
            release_path=release_path,
            role=role,
            origin=origin,
            license_treatment=license_treatment,
            reason_included=reason_included,
            sanitized=True,
        )
    )


def copy_items(items: list[ReleaseItem], release_dir: Path) -> None:
    for item in items:
        if item.source_path == "<generated>":
            continue
        target = release_dir / item.release_path
        target.parent.mkdir(parents=True, exist_ok=True)
        source = source_for_item(item)
        if source.exists() and source.is_file():
            shutil.copy2(source, target)
            sanitize_release_copy(target)


def source_for_item(item: ReleaseItem) -> Path:
    if item.sanitized:
        return PREFLIGHT / "_sanitized" / item.release_path
    return ROOT / item.source_path


def sanitize_notebook_manifest(data: dict[str, Any]) -> dict[str, Any]:
    sanitized = dict(data)
    sanitized.update(
        {
            "agent_path": "kaggle/notebook_candidate/my_agent.py",
            "notebook_path": "kaggle/notebook_candidate/arc3_object_substrate_submission.ipynb",
            "package_payload_path": "kaggle/package_candidate/substrate_plans.json",
            "source_sample_notebook": (
                "Kaggle sample ARC3 Sample Submission - Random Agent, version 13"
            ),
            "release_manifest_sanitized": True,
        }
    )
    return sanitized


def should_exclude(path: Path) -> bool:
    return (
        any(part in EXCLUDED_NAMES for part in path.parts)
        or path.name in EXCLUDED_NAMES
        or path.suffix in EXCLUDED_SUFFIXES
    )


def key_evidence_paths() -> list[str]:
    metadata_path = ROOT / "docs/paper/submission_candidate_metadata.json"
    paths: list[str] = []
    if metadata_path.exists():
        metadata = json.loads(metadata_path.read_text())
        paths.extend(metadata.get("repo_relative_paths_collected", []))

    extra = [
        "artifacts/object_substrate_v0/gamma3a_third_game_substrate_audit/action_effect_audit.json",
        "artifacts/object_substrate_v0/gamma3a_third_game_substrate_audit/goal_evidence_audit.json",
        "artifacts/object_substrate_v0/gamma3a_third_game_substrate_audit/perception_audit.json",
        "artifacts/object_substrate_v0/gamma3a_third_game_substrate_audit/substrate_gap_classification.json",
    ]
    paths.extend(extra)

    intentionally_excluded = {"docs/paper/kaggle_linkage_plan.md"}
    result = []
    for path in paths:
        if path in intentionally_excluded:
            continue
        if path not in result:
            result.append(path)
    return result


def excluded_file_records() -> list[dict[str, str]]:
    return [
        {
            "source_path": "docs/paper/kaggle_linkage_plan.md",
            "reason": (
                "Historical planning doc intentionally excluded from the public package; "
                "submission_record.json and submission_readiness.md supersede it for the "
                "Kaggle linkage evidence. The paper URL update remains pending until a "
                "public repo exists."
            ),
        },
        {
            "source_path": "artifacts/kaggle_submission_preflight/kaggle_submission_record/object_substrate_kaggle_candidate_upload.zip",
            "reason": "Binary upload archive excluded; source package and notebook files are included instead.",
        },
        {
            "source_path": "private repo history",
            "reason": "Fresh public repo candidate must be created without private git history.",
        },
        {
            "source_path": "browser/session artifacts",
            "reason": "Local sessions, cookies, and browser state are not reproducibility artifacts.",
        },
    ]


def build_kaggle_status_check(
    generated_at: str,
    skip_network: bool,
    browser_inspected: bool,
    browser_status: str | None,
    browser_score: str | None,
    browser_notebook_visibility: str | None,
) -> dict[str, Any]:
    record_path = ROOT / "artifacts/kaggle_submission_preflight/kaggle_submission_record/submission_record.json"
    record = json.loads(record_path.read_text()) if record_path.exists() else {}
    row = record.get("observed_submission_row", {})
    status = str(row.get("status", record.get("kaggle_submission_status", "")))
    score = row.get("public_score", record.get("linked_kaggle_score"))
    public_url = record.get("notebook_url", KAGGLE_NOTEBOOK_URL)
    public_check = check_public_url(public_url, skip_network=skip_network)
    observed_status_values = {status.lower()}
    if browser_status:
        observed_status_values.add(browser_status.lower())

    return {
        "kind": "kaggle_status_check",
        "schema_version": "v0",
        "generated_at": generated_at,
        "inspection_sources": ["local_submission_record", "unauthenticated_public_url_probe"],
        "signed_in_browser_inspection_performed": browser_inspected,
        "signed_in_browser_observation": {
            "submission_status": browser_status,
            "public_score": browser_score,
            "notebook_visibility": browser_notebook_visibility,
            "notes": (
                "Read-only Chrome inspection of Kaggle notebook/submissions pages; "
                "no submit action was taken."
                if browser_inspected
                else None
            ),
        },
        "kaggle_submission_exists": bool(record),
        "accepted_or_succeeded": bool(
            observed_status_values & {"succeeded", "submitted_succeeded", "accepted"}
        ),
        "score_observed": score,
        "public_url": public_url,
        "public_access_verified": public_check["ok"],
        "public_access_check": public_check,
        "errors_or_warnings": kaggle_warnings(
            record,
            public_check,
            browser_inspected=browser_inspected,
        ),
        "no_new_submission_made": True,
    }


def kaggle_warnings(
    record: dict[str, Any],
    public_check: dict[str, Any],
    *,
    browser_inspected: bool,
) -> list[str]:
    warnings: list[str] = []
    if not record:
        warnings.append("missing_local_submission_record")
    if not public_check["ok"]:
        warnings.append("kaggle_public_url_not_verified")
    if not browser_inspected:
        warnings.append("signed_in_browser_status_not_verified_by_this_script")
    return warnings


def build_rule_snapshot(generated_at: str, skip_network: bool) -> dict[str, Any]:
    checks = {name: check_public_url(url, skip_network=skip_network) for name, url in RULE_SOURCE_URLS.items()}
    return {
        "kind": "arc_prize_rule_snapshot",
        "schema_version": "v0",
        "generated_at": generated_at,
        "source_urls": RULE_SOURCE_URLS,
        "source_fetch_status": checks,
        "requirements_observed": {
            "paper_kaggle_linkage": (
                "Paper submissions must link to a Kaggle code submission for ARC-AGI-2 "
                "or ARC-AGI-3; the linked code submission need not achieve a high score "
                "for paper eligibility."
            ),
            "accuracy_category": (
                "The linked submission score is used for the paper rubric Accuracy category."
            ),
            "paper_contents": (
                "Expected paper contents include Abstract, Intro, Prior work, Approach, "
                "Results, and Conclusion; shorter and clearer is preferred."
            ),
            "open_source_license": (
                "Submitter-authored code and methods must be open sourced under a "
                "permissive public-domain-style license such as CC0 or MIT-0."
            ),
            "third_party_license": (
                "Third-party code or methods must be available under at least an "
                "open-source license allowing public sharing."
            ),
            "kaggle_track_requirements": (
                "ARC-AGI-3 submissions must be made through Kaggle, have no internet "
                "access during evaluation, and must open-source code/methods for prize eligibility."
            ),
            "scoring_methodology": (
                "ARC-AGI-3 scores completion and action efficiency; internal reasoning "
                "or tool calls that do not affect game state are not counted as actions."
            ),
        },
        "snapshot_caveat": (
            "Internal preflight summary, not legal advice. Re-check official rules before submission."
        ),
    }


def build_license_audit(generated_at: str, inventory: dict[str, Any]) -> dict[str, Any]:
    closure_path = ROOT / "artifacts/kaggle_submission_preflight/license_dependency_closure/closure_report.json"
    inventory_path = (
        ROOT / "artifacts/kaggle_submission_preflight/license_dependency_closure/"
        "third_party_dependency_inventory.json"
    )
    closure = json.loads(closure_path.read_text()) if closure_path.exists() else {}
    third_party = json.loads(inventory_path.read_text()) if inventory_path.exists() else {}
    unknowns = [
        item
        for item in inventory["included_files"]
        if item["origin"] == "unknown" or item["license_treatment"] == "blocker_unknown"
    ]
    notebook_imports = build_notebook_import_inventory()

    return {
        "kind": "public_release_license_audit",
        "schema_version": "v0",
        "generated_at": generated_at,
        "recommended_submitter_license": "MIT-0",
        "whether_root_private_repo_license_needs_to_change": "no",
        "whether_release_candidate_package_level_license_is_sufficient": "yes",
        "source_license_inputs": {
            "root_license": "Apache-2.0",
            "package_candidate_license": "MIT No Attribution / MIT-0-style",
            "closure_report": rel(closure_path) if closure_path.exists() else None,
        },
        "third_party_inventory": third_party,
        "kaggle_notebook_import_inventory": notebook_imports,
        "prior_closure_summary": closure,
        "unknown_license_blockers": unknowns,
        "files_needing_human_legal_review": [
            "Release license posture is a preliminary internal engineering audit, not legal advice.",
            (
                "The Kaggle notebook depends on competition-provided ARC-AGI-3 wheels "
                "and starter-agent modules at evaluation time. They are not vendored "
                "into this release candidate, but their license/competition terms should "
                "be rechecked before final prize submission."
            ),
        ],
        "cautious_language": "preliminary internal license posture, not legal advice",
    }


def build_scan_report(generated_at: str, release_dir: Path) -> dict[str, Any]:
    local_path_hits: list[dict[str, str]] = []
    secret_hits: list[dict[str, str]] = []
    forbidden_claim_hits: list[dict[str, str]] = []
    stale_score_hits: list[dict[str, str]] = []
    scanned_files = 0

    for path in sorted(release_dir.rglob("*")):
        if not path.is_file() or is_binary(path):
            continue
        scanned_files += 1
        text = path.read_text(errors="ignore")
        lines = text.splitlines()
        rel_path = rel(path)
        for name, pattern in LOCAL_PATH_PATTERNS.items():
            for line_no, line in matching_lines(text, pattern):
                if not is_allowed_local_path_guard_literal(line):
                    local_path_hits.append({"file": rel_path, "line": str(line_no), "pattern": name, "text": line})
        for name, regex in SECRET_PATTERNS.items():
            for line_no, line in regex_matching_lines(text, regex):
                secret_hits.append({"file": rel_path, "line": str(line_no), "pattern": name, "text": scrub_secret_line(line)})
        for phrase in FORBIDDEN_CLAIM_PATTERNS:
            for line_no, line in matching_lines(text, phrase):
                context = "\n".join(lines[max(0, line_no - 4) : line_no])
                if not is_allowed_forbidden_phrase_context(line, context):
                    forbidden_claim_hits.append({"file": rel_path, "line": str(line_no), "phrase": phrase, "text": line})
        for phrase in STALE_SCORE_PATTERNS:
            for line_no, line in matching_lines(text, phrase):
                if not is_allowed_stale_score_guard_literal(line):
                    stale_score_hits.append({"file": rel_path, "line": str(line_no), "phrase": phrase, "text": line})

    link_scan = build_link_scan(release_dir)
    return {
        "kind": "public_release_scan_report",
        "schema_version": "v0",
        "generated_at": generated_at,
        "release_directory": rel(release_dir),
        "scanned_text_file_count": scanned_files,
        "secrets_scan_status": "pass" if not secret_hits else "fail",
        "local_path_scan_status": "pass" if not local_path_hits else "fail",
        "forbidden_claim_scan_status": "pass" if not forbidden_claim_hits else "fail",
        "stale_score_terminology_status": "pass" if not stale_score_hits else "warning",
        "link_scan_status": link_scan["status"],
        "link_scan": link_scan,
        "secret_hits": secret_hits,
        "local_path_hits": local_path_hits,
        "forbidden_claim_hits": forbidden_claim_hits,
        "stale_score_hits": stale_score_hits,
    }


def build_evidence_path_audit(generated_at: str, inventory: dict[str, Any]) -> dict[str, Any]:
    release_by_source = {
        item["source_path"]: item["release_path"]
        for item in inventory["included_files"]
        if item["source_path"] != "<generated>"
    }
    metadata_path = ROOT / "docs/paper/submission_candidate_metadata.json"
    collected = []
    if metadata_path.exists():
        collected = json.loads(metadata_path.read_text()).get("repo_relative_paths_collected", [])

    intentionally_excluded = {
        record["source_path"]: record["reason"] for record in inventory["excluded_files"]
    }
    audited = []
    missing = []
    for source_path in collected:
        source_exists = (ROOT / source_path).exists()
        release_path = release_by_source.get(source_path)
        if release_path:
            status = "included"
        elif source_path in intentionally_excluded:
            status = "intentionally_excluded"
        else:
            status = "missing_from_release_candidate"
            missing.append(source_path)
        audited.append(
            {
                "source_path": source_path,
                "source_exists": source_exists,
                "release_path": release_path,
                "status": status,
                "reason": intentionally_excluded.get(source_path),
            }
        )

    return {
        "kind": "public_release_evidence_path_audit",
        "schema_version": "v0",
        "generated_at": generated_at,
        "metadata_source": rel(metadata_path),
        "total_evidence_paths": len(collected),
        "included_count": sum(1 for item in audited if item["status"] == "included"),
        "intentionally_excluded_count": sum(
            1 for item in audited if item["status"] == "intentionally_excluded"
        ),
        "missing_count": len(missing),
        "missing_paths": missing,
        "evidence_path_status": "pass" if not missing else "fail",
        "audited_paths": audited,
    }


def build_readiness_report(
    *,
    generated_at: str,
    output_dir: Path,
    inventory: dict[str, Any],
    kaggle_status: dict[str, Any],
    rule_snapshot: dict[str, Any],
    license_audit: dict[str, Any],
    scan_report: dict[str, Any],
    evidence_audit: dict[str, Any],
    skip_network: bool,
    github_publish_recorded: bool,
) -> dict[str, Any]:
    public_repo_check = check_public_url(PROPOSED_REPO_URL, skip_network=skip_network)
    current_repo_check = check_public_url(CURRENT_PRIVATE_REPO_URL, skip_network=skip_network)

    blockers: list[str] = []
    warnings: list[str] = []
    if not kaggle_status["accepted_or_succeeded"]:
        blockers.append("kaggle_submission_not_accepted_or_succeeded")
    if not kaggle_status["public_access_verified"]:
        blockers.append("kaggle_public_url_not_verified")
    if not public_repo_check["ok"]:
        blockers.append("proposed_public_repo_url_not_published_or_not_public")
    if scan_report["secrets_scan_status"] != "pass":
        blockers.append("release_candidate_secret_scan_failed")
    if scan_report["local_path_scan_status"] != "pass":
        blockers.append("release_candidate_local_path_scan_failed")
    if scan_report["forbidden_claim_scan_status"] != "pass":
        blockers.append("release_candidate_forbidden_claim_scan_failed")
    if scan_report["link_scan_status"] != "pass":
        blockers.append("release_candidate_link_scan_failed")
    if evidence_audit["evidence_path_status"] != "pass":
        blockers.append("release_candidate_evidence_paths_missing")
    if license_audit["unknown_license_blockers"]:
        blockers.append("release_candidate_unknown_license_blockers")
    if scan_report["stale_score_terminology_status"] != "pass":
        warnings.append("release_candidate_has_stale_score_terminology_warnings")
    if not rule_snapshot["source_fetch_status"]["paper_prize"]["ok"]:
        warnings.append("paper_prize_rule_url_not_fetch_verified_by_script")

    ready = not blockers
    return {
        "kind": "public_release_preflight_readiness_report",
        "schema_version": "v0",
        "generated_at": generated_at,
        "public_release_ready": ready,
        "blocking_issues": blockers,
        "warnings": warnings,
        "proposed_public_repo_name": PROPOSED_REPO_NAME,
        "proposed_public_repo_url": PROPOSED_REPO_URL,
        "release_directory": rel(output_dir / RELEASE_DIR_NAME),
        "included_files": [item["release_path"] for item in inventory["included_files"]],
        "excluded_files": inventory["excluded_files"],
        "license_status": {
            "recommended_submitter_license": license_audit["recommended_submitter_license"],
            "package_level_license_sufficient": license_audit[
                "whether_release_candidate_package_level_license_is_sufficient"
            ],
            "root_private_repo_license_needs_change": license_audit[
                "whether_root_private_repo_license_needs_to_change"
            ],
        },
        "third_party_status": {
            "unknown_license_blockers": license_audit["unknown_license_blockers"],
            "human_legal_review_note": license_audit["files_needing_human_legal_review"],
        },
        "secrets_scan_status": scan_report["secrets_scan_status"],
        "local_path_scan_status": scan_report["local_path_scan_status"],
        "forbidden_claim_scan_status": scan_report["forbidden_claim_scan_status"],
        "link_scan_status": scan_report["link_scan_status"],
        "evidence_path_status": evidence_audit["evidence_path_status"],
        "kaggle_link_status": {
            "accepted_or_succeeded": kaggle_status["accepted_or_succeeded"],
            "score_observed": kaggle_status["score_observed"],
            "public_url": kaggle_status["public_url"],
            "public_access_verified": kaggle_status["public_access_verified"],
        },
        "github_public_access_status": {
            "proposed_public_repo_url": public_repo_check,
            "current_private_repo_url": current_repo_check,
        },
        "github_publish_authorization_required": not github_publish_recorded,
        "paper_url_update_pending": scan_report["link_scan_status"] != "pass",
        "no_github_repo_published": not github_publish_recorded,
        "no_kaggle_submission_made": True,
        "no_paper_submission_made": True,
        "no_official_arc_run_invoked": True,
        "no_new_capability_claim_made": True,
        "recommended_next_action": recommended_next_action(
            ready,
            blockers,
            github_publish_recorded=github_publish_recorded,
        ),
    }


def recommended_next_action(
    ready: bool,
    blockers: list[str],
    *,
    github_publish_recorded: bool,
) -> str:
    if ready:
        if github_publish_recorded:
            return "hold_for_cold_read_and_final_submission_checklist"
        return "ask_tim_for_explicit_authorization_to_publish_fresh_public_github_repo"
    if "kaggle_submission_not_accepted_or_succeeded" in blockers:
        return "stop_and_resolve_kaggle_linkage_before_public_release"
    if "proposed_public_repo_url_not_published_or_not_public" in blockers:
        return "review_release_candidate_then_request_authorization_to_publish_fresh_public_repo"
    return "fix_blocking_preflight_issues_before_paper_submission"


def build_trajectory_record(
    generated_at: str,
    output_dir: Path,
    readiness: dict[str, Any],
) -> dict[str, Any]:
    return {
        "kind": "public_release_preflight_trajectory_record",
        "schema_version": "v0",
        "generated_at": generated_at,
        "steps": [
            "inspected existing paper and Kaggle/package artifacts",
            "created local release candidate without private git history",
            "sanitized notebook manifest absolute paths in release copy",
            "generated inventory, license, scan, evidence, rule, and readiness reports",
            "stopped before GitHub publication, Kaggle submission, paper submission, and official ARC runs",
        ],
        "output_dir": rel(output_dir),
        "readiness_public_release_ready": readiness["public_release_ready"],
        "blocking_issues": readiness["blocking_issues"],
    }


def build_public_release_plan(
    readiness: dict[str, Any],
    license_audit: dict[str, Any],
    evidence_audit: dict[str, Any],
) -> str:
    if readiness["no_github_repo_published"]:
        publication_status = (
            "It is a preflight plan only: no GitHub repository has been\n"
            "published, no Kaggle submission has been made, no paper has been submitted, and\n"
            "no official ARC run has been invoked."
        )
        github_steps_heading = "Manual GitHub Steps"
        github_steps_body = f"""1. Create a new empty public GitHub repository named `{PROPOSED_REPO_NAME}`.
2. Copy the contents of `{readiness["release_directory"]}` into that new repository.
3. Commit with a message such as `Initial ARC-AGI-3 paper release package`.
4. Push to GitHub.
5. Open `{PROPOSED_REPO_URL}` in an unauthenticated/incognito browser.
6. Confirm `README.md`, `LICENSE`, `paper/submission_candidate.pdf`, and the key
   evidence paths are visible."""
    else:
        publication_status = (
            "The fresh public GitHub repository has been published from the clean\n"
            "release candidate. No new Kaggle submission has been made, no paper has been\n"
            "submitted, and no official ARC run has been invoked."
        )
        github_steps_heading = "Completed GitHub Publication"
        github_steps_body = f"""- Published repository: `{PROPOSED_REPO_URL}`
- Published source: `{readiness["release_directory"]}`
- Private repository history was not published.
- Post-publish checks should confirm `README.md`, `LICENSE`,
  `paper/submission_candidate.pdf`, and the key evidence paths remain visible."""

    return f"""# Public Release Plan

This plan prepares a fresh public repository for the ARC-AGI-3 Paper Prize
submission package. {publication_status}

## Proposed Public Repository

- Name: `{PROPOSED_REPO_NAME}`
- URL: `{PROPOSED_REPO_URL}`
- Local release candidate: `{readiness["release_directory"]}`

Use a fresh public repository with no private git history. Do not make the full
private workspace public.

## License

- Recommended submitter-authored release license: `{license_audit["recommended_submitter_license"]}`
- Root private repository license change required: `{license_audit["whether_root_private_repo_license_needs_to_change"]}`
- Release-candidate package-level license sufficient: `{license_audit["whether_release_candidate_package_level_license_is_sufficient"]}`

This is a preliminary internal license posture and not legal advice.

## Files To Publish

Publish the local release candidate directory as the repository root:

- `README.md`, `LICENSE`, `NOTICE`, `THIRD_PARTY_LICENSES.md`
- `paper/` reader-clean paper artifacts
- `kaggle/` package, notebook, and submission-linkage artifacts
- `artifacts/` key receipts cited by the paper
- `docs/` supporting paper/object-substrate docs included in the evidence path audit
- `tools/` and `tests/` needed to reproduce the paper candidate and release preflight

Evidence path audit status: `{evidence_audit["evidence_path_status"]}`.

## {github_steps_heading}

{github_steps_body}

## Paper URL Update Steps

After the public repo URL resolves:

1. Confirm the already-staged paper URL still points at `{PROPOSED_REPO_URL}`.
2. Re-run paper and public-release tests.
3. Re-check the GitHub and Kaggle links in an unauthenticated/incognito browser.

## Forbidden Claims

The public release must not claim:

- private-eval capability
- a general ARC-AGI-3 solver
- autonomous substrate discovery
- a positive Kaggle leaderboard result
- all-level capability on any game

The preserved claim boundary is: Kaggle public score `0.0`, public-scorecard
level-1 capability on `ls20` and `tr87`, and method characterization across
`ls20`, `tr87`, and `cn04`.
"""


def release_readme(generated_at: str) -> str:
    return f"""# ARC-AGI-3 Substrate Discovery Paper Release Package

Generated: {generated_at}

This package is the clean public-release surface for the paper
**Failure-Driven Substrate Discovery for ARC-AGI-3**. It is prepared for the
fresh public repository at `{PROPOSED_REPO_URL}` without private git history.

## Claim Boundary

- Linked Kaggle public score: `0.0`
- Public-scorecard capability: `ls20` and `tr87` level 1
- Method characterization: `ls20`, `tr87`, and `cn04`
- No private-eval capability claim
- No general ARC-AGI-3 solver claim
- No autonomous substrate discovery claim
- No all-level capability claim

## Reproducibility Surface

- `paper/` contains the reader-clean paper candidate and claim-support docs.
- `kaggle/` contains the package/notebook/submission-record surface tied to the
  linked Kaggle entry.
- `artifacts/` and `docs/` contain key receipts and summaries cited by the paper.
- `tools/` and `tests/` contain local guards for regenerating and checking the
  paper/release artifacts.

## Suggested Checks

From a repository root containing this release candidate:

```bash
python tools/paper/build_submission_candidate.py --output-dir /tmp/arc3-paper-check
pytest -q tests/test_paper_submission_candidate.py tests/test_public_release_preflight.py
```

The original private repository history is intentionally not included.
"""


def check_public_url(url: str, *, skip_network: bool) -> dict[str, Any]:
    if skip_network:
        return {"ok": False, "status": "skipped", "url": url, "error": "network_check_skipped"}
    request = urllib.request.Request(url, headers={"User-Agent": "arc3-release-preflight/0"})
    try:
        with urllib.request.urlopen(request, timeout=12) as response:
            return {
                "ok": 200 <= response.status < 400,
                "status": response.status,
                "url": url,
                "final_url": response.url,
            }
    except urllib.error.HTTPError as exc:
        return {"ok": False, "status": exc.code, "url": url, "error": str(exc)}
    except Exception as exc:  # pragma: no cover - network-specific failure details
        return {"ok": False, "status": "error", "url": url, "error": str(exc)}


def build_notebook_import_inventory() -> dict[str, Any]:
    notebook = ROOT / "artifacts/kaggle_submission_preflight/kaggle_notebook_candidate/arc3_object_substrate_submission.ipynb"
    agent = ROOT / "artifacts/kaggle_submission_preflight/kaggle_notebook_candidate/my_agent.py"
    imported_modules: set[str] = set()
    pip_install_mentions: set[str] = set()

    if agent.exists():
        imported_modules.update(extract_imports(agent.read_text()))
    if notebook.exists():
        data = json.loads(notebook.read_text())
        for cell in data.get("cells", []):
            source = "".join(cell.get("source", []))
            if cell.get("cell_type") == "code":
                imported_modules.update(extract_imports(source))
                if "pip install" in source:
                    pip_install_mentions.update(
                        re.findall(r"\b(arc-agi|python-dotenv|pandas)\b", source)
                    )

    runtime_third_party = []
    for module in sorted(imported_modules | pip_install_mentions):
        if module in {"__future__", "json", "os", "time", "typing"}:
            continue
        runtime_third_party.append(
            {
                "module_or_package": module,
                "scope": third_party_scope(module),
                "redistributed_in_release_candidate": False,
                "license_posture": third_party_license_posture(module),
            }
        )

    return {
        "source_files": [rel(path) for path in [notebook, agent] if path.exists()],
        "imported_modules": sorted(imported_modules),
        "pip_install_mentions": sorted(pip_install_mentions),
        "runtime_third_party": runtime_third_party,
        "coverage_note": (
            "This inventory covers the Kaggle notebook and generated my_agent.py "
            "imports. Competition-provided ARC runtime code is referenced, not vendored."
        ),
    }


def extract_imports(source: str) -> set[str]:
    imports: set[str] = set()
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return imports
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".")[0])
    return imports


def third_party_scope(module: str) -> str:
    if module in {"arcengine", "agents", "arc-agi", "python-dotenv"}:
        return "Kaggle ARC-AGI-3 competition runtime"
    if module == "pandas":
        return "Kaggle base notebook environment for non-rerun dummy submission"
    return "unknown_or_stdlib_review"


def third_party_license_posture(module: str) -> str:
    if module in {"arcengine", "agents", "arc-agi", "python-dotenv"}:
        return "competition-provided runtime dependency, not redistributed; recheck competition license before final submission"
    if module == "pandas":
        return "Kaggle base environment dependency, not redistributed"
    return "requires review"


def build_link_scan(release_dir: Path) -> dict[str, Any]:
    stale_private_repo_url_hits: list[dict[str, str]] = []
    proposed_repo_url_hits: list[dict[str, str]] = []
    kaggle_url_hits: list[dict[str, str]] = []

    def scan_text(rel_path: str, text: str) -> None:
        for line_no, line in matching_lines(text, CURRENT_PRIVATE_REPO_URL):
            if not is_allowed_stale_repo_url_guard_literal(line):
                stale_private_repo_url_hits.append({"file": rel_path, "line": str(line_no), "text": line})
        for line_no, line in matching_lines(text, PROPOSED_REPO_URL):
            proposed_repo_url_hits.append({"file": rel_path, "line": str(line_no), "text": line})
        for line_no, line in matching_lines(text, KAGGLE_NOTEBOOK_URL):
            kaggle_url_hits.append({"file": rel_path, "line": str(line_no), "text": line})

    for path in sorted(release_dir.rglob("*")):
        if not path.is_file() or is_binary(path):
            continue
        scan_text(rel(path), path.read_text(errors="ignore"))

    pdf_path = release_dir / "paper/submission_candidate.pdf"
    pdf_text_status = "not_present"
    if pdf_path.exists():
        pdf_text = extract_pdf_text(pdf_path)
        pdf_text_status = "checked" if pdf_text is not None else "extract_failed"
        if pdf_text:
            scan_text(rel(pdf_path), pdf_text)

    metadata = release_dir / "paper/submission_candidate_metadata.json"
    metadata_repo_url = None
    if metadata.exists():
        metadata_repo_url = json.loads(metadata.read_text()).get("repo_url")

    status = "pass"
    reasons: list[str] = []
    if stale_private_repo_url_hits:
        status = "fail"
        reasons.append("release_candidate_contains_current_private_repo_url")
    if metadata_repo_url != PROPOSED_REPO_URL:
        status = "fail"
        reasons.append("paper_metadata_repo_url_not_final_public_repo_url")
    if not proposed_repo_url_hits:
        status = "fail"
        reasons.append("proposed_public_repo_url_absent_from_release_text")
    if not kaggle_url_hits:
        status = "fail"
        reasons.append("kaggle_notebook_url_absent_from_release_text")

    return {
        "status": status,
        "reasons": reasons,
        "metadata_repo_url": metadata_repo_url,
        "required_repo_url": PROPOSED_REPO_URL,
        "kaggle_notebook_url": KAGGLE_NOTEBOOK_URL,
        "stale_private_repo_url_hits": stale_private_repo_url_hits,
        "proposed_repo_url_hit_count": len(proposed_repo_url_hits),
        "kaggle_url_hit_count": len(kaggle_url_hits),
        "pdf_text_status": pdf_text_status,
        "resolution_note": (
            "This checks that the release candidate points at the final public repo URL. "
            "Actual public URL resolution remains a separate readiness blocker until the "
            "fresh GitHub repo is published and the Kaggle notebook is public/shareable."
        ),
    }


def extract_pdf_text(path: Path) -> str | None:
    try:
        from pypdf import PdfReader
    except Exception:
        return None
    try:
        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception:
        return None


def matching_lines(text: str, pattern: str) -> list[tuple[int, str]]:
    needle = pattern.lower()
    return [
        (line_no, line.strip())
        for line_no, line in enumerate(text.splitlines(), start=1)
        if needle in line.lower()
    ]


def regex_matching_lines(text: str, regex: re.Pattern[str]) -> list[tuple[int, str]]:
    return [
        (line_no, line.strip())
        for line_no, line in enumerate(text.splitlines(), start=1)
        if regex.search(line)
    ]


def is_negated_claim_line(line: str) -> bool:
    low = line.lower()
    return any(word in low for word in NEGATING_WORDS)


def is_allowed_forbidden_phrase_context(line: str, context: str) -> bool:
    stripped = line.strip()
    if is_negated_claim_line(line):
        return True
    low_context = context.lower()
    if "forbidden claim" in low_context or "must not claim" in low_context:
        return True
    if stripped.startswith('"') and stripped.endswith(('",', '"')):
        return True
    if stripped.startswith("'") and stripped.endswith(("',", "'")):
        return True
    return False


def is_allowed_local_path_guard_literal(line: str) -> bool:
    stripped = line.strip()
    if stripped.startswith('"') and stripped.endswith(('",', '"')):
        return True
    if f'"{LOCAL_PATH_PATTERNS["users_path"]}" not in' in stripped:
        return True
    if f'"{LOCAL_PATH_PATTERNS["mnt_data_path"]}" not in' in stripped:
        return True
    if "localhost_assumption" in stripped:
        return True
    if '"localhost"' in stripped and (
        "LOCAL_PATH_PATTERNS" in stripped
        or "in stripped" in stripped
    ):
        return True
    return False


def is_allowed_stale_score_guard_literal(line: str) -> bool:
    stripped = line.strip()
    if stripped.startswith('"') and stripped.endswith(('",', '"')):
        return True
    if "STALE_SCORE_PATTERNS" in stripped:
        return True
    return False


def is_allowed_stale_repo_url_guard_literal(line: str) -> bool:
    stripped = line.strip()
    if "CURRENT_PRIVATE_REPO_URL" in stripped:
        return True
    if "not in text" in stripped:
        return True
    return False


def sanitize_release_copy(path: Path) -> None:
    if is_binary(path):
        return
    try:
        text = path.read_text()
    except UnicodeDecodeError:
        return
    home = Path.home()
    replacements = {
        f"{ROOT}/": "",
        str(ROOT): ".",
        f"{home / CURRENT_PRIVATE_REPO_NAME}/": f"{CURRENT_PRIVATE_REPO_NAME}/",
        str(home / CURRENT_PRIVATE_REPO_NAME): CURRENT_PRIVATE_REPO_NAME,
        f"{home / 'ARC-AGI-3-Agents'}/": "ARC-AGI-3-Agents/",
        str(home / "ARC-AGI-3-Agents"): "ARC-AGI-3-Agents",
        f"{home / 'Downloads'}/": "local_downloads/",
        str(home / "Downloads"): "local_downloads",
    }
    clean = text
    for before, after in replacements.items():
        clean = clean.replace(before, after)
    if clean != text:
        path.write_text(clean)


def scrub_secret_line(line: str) -> str:
    scrubbed = line
    for regex in SECRET_PATTERNS.values():
        scrubbed = regex.sub("<redacted>", scrubbed)
    return scrubbed.strip()


def is_binary(path: Path) -> bool:
    return path.suffix.lower() in {".pdf", ".zip", ".png", ".jpg", ".jpeg", ".gif"}


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def rel(path: Path | str) -> str:
    path = Path(path)
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


if __name__ == "__main__":
    main()
