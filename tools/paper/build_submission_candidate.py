from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import shutil
from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "docs" / "paper"
MANUSCRIPT = PAPER / "manuscript_v1.md"
REFERENCES = PAPER / "references.md"
CLAIMS = PAPER / "claim_inventory.md"
READER_MD = PAPER / "submission_manuscript.md"
PDF = PAPER / "submission_candidate.pdf"
METADATA = PAPER / "submission_candidate_metadata.json"
PAPER_TITLE = "Failure-Driven Substrate Discovery for ARC-AGI-3"
OUTPUT_FILENAMES = {
    "reader_markdown": "submission_manuscript.md",
    "pdf": "submission_candidate.pdf",
    "metadata": "submission_candidate_metadata.json",
}

REPO_URL = "https://github.com/Haserjian/arc3-substrate-discovery-paper"
KAGGLE_NOTEBOOK_URL = (
    "https://www.kaggle.com/code/timhaserjian/"
    "arc3-object-substrate-submission-candidate"
)
INTERNAL_FRONTMATTER_FLAGS = [
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
]
REFERENCE_KEYS = [
    "ARCPrize2026Paper",
    "ARCAGI3Methodology",
    "ARCAGI3Track",
    "ARCAGI3Benchmark2026",
    "Rodionov2026EWM",
    "RudakovEtAl2025Graph",
    "LiuEtAl2026MAP",
]
PATH_PREFIXES = (
    "artifacts/",
    "docs/",
    "tests/",
    "kaggle/",
    "object_substrate_v0/",
    "planner_v0/",
    "agents/",
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-url", default=REPO_URL)
    parser.add_argument("--kaggle-url", default=KAGGLE_NOTEBOOK_URL)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PAPER,
        help="Directory for generated submission_manuscript.md, submission_candidate.pdf, and metadata.",
    )
    args = parser.parse_args()
    output_dir = resolve_output_dir(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    reader_md = output_dir / OUTPUT_FILENAMES["reader_markdown"]
    pdf_path = output_dir / OUTPUT_FILENAMES["pdf"]
    metadata_path = output_dir / OUTPUT_FILENAMES["metadata"]

    manuscript = MANUSCRIPT.read_text()
    references = REFERENCES.read_text()
    claim_inventory = CLAIMS.read_text()

    reader_text, used_claims, repo_paths = build_reader_markdown(
        manuscript=manuscript,
        references=references,
        claim_inventory=claim_inventory,
        repo_url=args.repo_url,
        kaggle_url=args.kaggle_url,
    )
    reader_md.write_text(reader_text)

    render_pdf(reader_text, pdf_path)
    page_count = pdf_page_count(pdf_path)

    metadata = build_metadata(
        manuscript=manuscript,
        reader_text=reader_text,
        used_claims=used_claims,
        repo_paths=repo_paths,
        page_count=page_count,
        repo_url=args.repo_url,
        kaggle_url=args.kaggle_url,
        reader_md=reader_md,
        pdf_path=pdf_path,
    )
    metadata_path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n")


def resolve_output_dir(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def build_reader_markdown(
    *,
    manuscript: str,
    references: str,
    claim_inventory: str,
    repo_url: str,
    kaggle_url: str,
) -> tuple[str, list[str], list[str]]:
    body = strip_frontmatter(manuscript).lstrip()
    body = remove_internal_status_notes(body)

    repo_paths = unique_repo_paths(manuscript)
    body = clean_internal_parentheticals(body)
    body = clean_remaining_repo_paths(body)
    body = normalize_claim_range_language(body)

    used_claims = used_claim_ids(manuscript)
    reference_section = format_references(references)
    appendix = format_claim_appendix(claim_inventory, used_claims)
    reproducibility = format_reproducibility_section(repo_paths, repo_url, kaggle_url)

    body = body.rstrip()
    clean = "\n\n".join([body, reproducibility, appendix, reference_section]).rstrip() + "\n"
    return clean, used_claims, repo_paths


def strip_frontmatter(text: str) -> str:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[end + len("\n---\n") :]
    return text


def remove_internal_status_notes(text: str) -> str:
    text = re.sub(
        r"\nThis is manuscript v1\..*?scorecard completions below remain separate capability evidence for covered\npublic games\.\n",
        "\n",
        text,
        flags=re.DOTALL,
    )
    text = re.sub(
        r"\nPrior work still needs final citation-style polish\..*?target venue format \([^)]*\)\.\n",
        "\n",
        text,
        flags=re.DOTALL,
    )
    return text


def clean_internal_parentheticals(text: str) -> str:
    pattern = re.compile(
        r"\((?=[^)]*(?:`C\d{2}`|`(?:artifacts|docs|tests|kaggle|object_substrate_v0|planner_v0|agents)/))[^)]*?\)",
        flags=re.DOTALL,
    )

    def replacement(match: re.Match[str]) -> str:
        value = match.group(0)
        claims = claim_mentions(value)
        if claims:
            return f"({format_claim_refs(claims)})"
        return "(repository artifacts listed in Data and Reproducibility Availability)"

    return pattern.sub(replacement, text)


def clean_remaining_repo_paths(text: str) -> str:
    path_pattern = re.compile(
        r"`((?:artifacts|docs|tests|kaggle|object_substrate_v0|planner_v0|agents)/[^`]+)`"
    )
    text = path_pattern.sub("the project repository", text)
    return re.sub(r"\s+\(\s*repository artifacts listed in Data and Reproducibility Availability\s*\)", "", text)


def normalize_claim_range_language(text: str) -> str:
    text = text.replace(
        "`C22` through `C40` cover",
        "the object-substrate claim range covers",
    )
    text = text.replace("`C22` through `C40`", "the object-substrate claim range")
    text = text.replace("`C02` through `C09`", "the early ls20 diagnostic claim range")
    return text


def claim_mentions(text: str) -> list[str]:
    claims = re.findall(r"`(C\d{2})`", text)
    range_match = re.search(r"`(C\d{2})`\s+through\s+`(C\d{2})`", text)
    if range_match:
        claims = [f"{range_match.group(1)}-{range_match.group(2)}"]
    return claims


def used_claim_ids(text: str) -> list[str]:
    explicit = set(re.findall(r"`(C\d{2})`", text))
    for start, end in re.findall(r"`C(\d{2})`\s+through\s+`C(\d{2})`", text):
        for number in range(int(start), int(end) + 1):
            explicit.add(f"C{number:02d}")
    return sorted(explicit)


def format_claim_refs(claims: list[str]) -> str:
    return "App. A, " + ", ".join(claims)


def unique_repo_paths(text: str) -> list[str]:
    paths = []
    for path in re.findall(
        r"`((?:artifacts|docs|tests|kaggle|object_substrate_v0|planner_v0|agents)/[^`]+)`",
        text,
    ):
        cleaned = path.rstrip(".,;:")
        if any(cleaned.startswith(prefix) for prefix in PATH_PREFIXES):
            paths.append(cleaned)
    return sorted(dict.fromkeys(paths))


def format_reproducibility_section(paths: list[str], repo_url: str, kaggle_url: str) -> str:
    key_paths = prioritize_paths(paths)
    lines = [
        "## Data and Reproducibility Availability",
        "",
        f"The source repository for the submitted method is {repo_url}. The linked Kaggle notebook is {kaggle_url}. Internal evidence is cited by repo-relative artifact paths rather than local filesystem paths; the submission candidate contains no local home-directory absolute paths.",
        "",
        "Key repo-relative evidence paths:",
        "",
    ]
    lines.extend(f"- {path}" for path in key_paths)
    return "\n".join(lines)


def prioritize_paths(paths: list[str]) -> list[str]:
    priority_terms = [
        "kaggle_submission_record",
        "run_005_object_aware_wall_fix/receipt.json",
        "tr87_run_001_object_aware/receipt.json",
        "gamma3a_third_game_substrate_audit",
        "cross_game_substrate_results.md",
        "substrate_gap_taxonomy.md",
        "claim_inventory.md",
        "results_table.md",
        "known_gaps.md",
        "references.md",
    ]
    selected: list[str] = []
    for term in priority_terms:
        for path in paths:
            if term in path and path not in selected:
                selected.append(path)
    for path in paths:
        if path not in selected:
            selected.append(path)
        if len(selected) >= 18:
            break
    return selected


def format_claim_appendix(claim_inventory: str, used_claims: list[str]) -> str:
    claims = parse_claim_inventory(claim_inventory)
    lines = [
        "## Appendix A: Claim Inventory Summary",
        "",
        "This appendix is a reader-facing index to the internal claim inventory. It is not a separate score claim; the full inventory in the repository carries artifacts, tests, and non-claim siblings.",
        "Reader summaries may shorten long machine identifiers for PDF legibility; exact identifiers are preserved in the repository inventory and receipts.",
        "",
        "| Claim ID | Tier | Reader summary |",
        "|---|---|---|",
    ]
    for claim_id in used_claims:
        item = claims.get(claim_id)
        if not item:
            continue
        summary = reader_claim_summary(item["claim"])
        lines.append(f"| {claim_id} | {item['tier']} | {summary} |")
    return "\n".join(lines)


def reader_claim_summary(claim: str) -> str:
    replacements = {
        "`official_local_online_divergence`": "an official/local online-divergence marker",
        "`method_transfers_ontology_doesnt`": "a method-transfers/ontology-does-not-transfer finding",
        "`sequence_rule_matching`": "sequence-rule matching",
        "`bsqsshqpox_sequence_rule_validation`": "the source-specific sequence-rule validation predicate",
        "`selector_position_change` and `sequence_state_change`": "selector-position and sequence-state effects",
        "`uses_motion_delta_representation: false`": "no motion-delta representation",
        "`ready_for_gamma2d_planner: false`": "planner readiness false",
        "`ready_for_gamma2d_planner: true`": "planner readiness true",
        "`prediction_mismatch_count: 0`": "zero prediction mismatches",
        "`provenance_complete: true`": "complete provenance",
    }
    for raw, replacement in replacements.items():
        claim = claim.replace(raw, replacement)
    return claim


def parse_claim_inventory(text: str) -> dict[str, dict[str, str]]:
    matches = list(re.finditer(r"^### (C\d{2}) - .+$", text, flags=re.MULTILINE))
    claims: dict[str, dict[str, str]] = {}
    for index, match in enumerate(matches):
        claim_id = match.group(1)
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        section = text[start:end]
        tier = first_field(section, "tier") or "UNKNOWN"
        claim = first_field(section, "claim") or match.group(0).replace(f"### {claim_id} - ", "")
        claims[claim_id] = {"tier": tier, "claim": claim}
    return claims


def first_field(section: str, field: str) -> str | None:
    match = re.search(rf"^- {field}: (.+)$", section, flags=re.MULTILINE)
    return match.group(1).strip() if match else None


def format_references(text: str) -> str:
    entries = parse_references(text)
    lines = ["## References", ""]
    for key in REFERENCE_KEYS:
        entry = entries[key]
        parts = [
            entry.get("authors_or_org", "Unknown author"),
            f"\"{entry.get('title', 'Untitled')}\"",
            entry.get("source", ""),
            entry.get("date", ""),
            entry.get("url", ""),
        ]
        arxiv_id = entry.get("arxiv_id")
        if arxiv_id:
            parts.insert(4, f"arXiv:{arxiv_id}")
        line = " ".join(part.strip().rstrip(".") + "." for part in parts if part.strip())
        lines.append(f"- [{key}] {line}")
    return "\n".join(lines)


def parse_references(text: str) -> dict[str, dict[str, str]]:
    matches = list(re.finditer(r"^## \[@([A-Za-z0-9]+)\]$", text, flags=re.MULTILINE))
    entries: dict[str, dict[str, str]] = {}
    for index, match in enumerate(matches):
        key = match.group(1)
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        section = text[start:end]
        values = {}
        for field in [
            "authors_or_org",
            "title",
            "source",
            "date",
            "url",
            "arxiv_id",
        ]:
            value = first_field(section, field)
            if value:
                values[field] = value
        entries[key] = values
    missing = set(REFERENCE_KEYS) - set(entries)
    if missing:
        raise ValueError(f"Missing references: {sorted(missing)}")
    return entries


def render_pdf(markdown_text: str, output_path: Path) -> None:
    try:
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.units import inch
        from reportlab.platypus import (
            SimpleDocTemplate,
            Spacer,
            Table,
            TableStyle,
            Paragraph,
        )
    except ImportError as exc:
        raise SystemExit(
            "ReportLab is required for the fallback PDF renderer. "
            "Use the bundled workspace Python or install reportlab."
        ) from exc

    styles = getSampleStyleSheet()
    body = ParagraphStyle(
        "PaperBody",
        parent=styles["BodyText"],
        fontName="Times-Roman",
        fontSize=9.4,
        leading=12.0,
        spaceAfter=5,
        wordWrap="CJK",
    )
    title = ParagraphStyle(
        "PaperTitle",
        parent=styles["Title"],
        fontName="Times-Bold",
        fontSize=18,
        leading=22,
        alignment=TA_CENTER,
        spaceAfter=8,
        wordWrap="CJK",
    )
    subtitle = ParagraphStyle(
        "PaperSubtitle",
        parent=body,
        fontName="Times-Italic",
        fontSize=11,
        leading=14,
        alignment=TA_CENTER,
        spaceAfter=14,
        wordWrap="CJK",
    )
    h2 = ParagraphStyle(
        "PaperHeading2",
        parent=styles["Heading2"],
        fontName="Times-Bold",
        fontSize=13,
        leading=16,
        spaceBefore=12,
        spaceAfter=6,
        wordWrap="CJK",
    )
    h3 = ParagraphStyle(
        "PaperHeading3",
        parent=styles["Heading3"],
        fontName="Times-Bold",
        fontSize=11,
        leading=13,
        spaceBefore=8,
        spaceAfter=4,
        wordWrap="CJK",
    )
    bullet = ParagraphStyle(
        "PaperBullet",
        parent=body,
        leftIndent=14,
        firstLineIndent=-8,
        spaceAfter=3,
        wordWrap="CJK",
    )
    table_cell = ParagraphStyle(
        "PaperTableCell",
        parent=body,
        fontSize=7.0,
        leading=8.5,
        spaceAfter=0,
        wordWrap="CJK",
    )
    table_header = ParagraphStyle(
        "PaperTableHeader",
        parent=table_cell,
        fontName="Times-Bold",
    )

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        rightMargin=0.72 * inch,
        leftMargin=0.72 * inch,
        topMargin=0.68 * inch,
        bottomMargin=0.68 * inch,
        title=PAPER_TITLE,
    )

    story = []
    lines = markdown_text.splitlines()
    paragraph: list[str] = []
    index = 0
    title_seen = False
    while index < len(lines):
        line = lines[index]
        if not line.strip():
            flush_paragraph(story, paragraph, body)
            index += 1
            continue
        if line.startswith("|"):
            flush_paragraph(story, paragraph, body)
            table_lines = []
            while index < len(lines) and lines[index].startswith("|"):
                table_lines.append(lines[index])
                index += 1
            story.append(markdown_table_to_flowable(table_lines, table_cell, table_header, doc.width))
            story.append(Spacer(1, 6))
            continue
        if line.startswith("# "):
            flush_paragraph(story, paragraph, body)
            story.append(Paragraph(inline(line[2:].strip()), title))
            title_seen = True
            index += 1
            continue
        if line.startswith("Subtitle:"):
            flush_paragraph(story, paragraph, body)
            subtitle_lines = []
            index += 1
            while index < len(lines) and lines[index].strip():
                subtitle_lines.append(lines[index].strip())
                index += 1
            if title_seen:
                story.append(Paragraph(inline(" ".join(subtitle_lines)), subtitle))
            continue
        if line.startswith("## "):
            flush_paragraph(story, paragraph, body)
            story.append(Paragraph(inline(line[3:].strip()), h2))
            index += 1
            continue
        if line.startswith("### "):
            flush_paragraph(story, paragraph, body)
            story.append(Paragraph(inline(line[4:].strip()), h3))
            index += 1
            continue
        if re.match(r"^\d+\. ", line):
            flush_paragraph(story, paragraph, body)
            story.append(Paragraph(inline(line.strip()), bullet))
            index += 1
            continue
        if line.startswith("- "):
            flush_paragraph(story, paragraph, body)
            story.append(Paragraph(inline(line.strip()), bullet))
            index += 1
            continue
        paragraph.append(line.strip())
        index += 1
    flush_paragraph(story, paragraph, body)

    def footer(canvas, document) -> None:
        canvas.saveState()
        canvas.setFont("Times-Roman", 8)
        canvas.drawCentredString(
            letter[0] / 2,
            0.38 * inch,
            f"{PAPER_TITLE} - {document.page}",
        )
        canvas.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


def flush_paragraph(story: list, lines: list[str], style) -> None:
    from reportlab.platypus import Paragraph

    if not lines:
        return
    text = " ".join(lines)
    story.append(Paragraph(inline(text), style))
    lines.clear()


def markdown_table_to_flowable(table_lines: list[str], cell_style, header_style, width: float):
    from reportlab.lib import colors
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import Paragraph, Table, TableStyle

    rows = []
    for line in table_lines:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if all(set(cell) <= {"-", ":", " "} for cell in cells):
            continue
        rows.append(cells)
    if not rows:
        return Paragraph("", cell_style)
    max_cols = max(len(row) for row in rows)
    normalized = [row + [""] * (max_cols - len(row)) for row in rows]
    col_widths = table_column_widths(normalized[0], width)
    body_style = cell_style
    head_style = header_style
    if normalized[0] == ["Claim ID", "Tier", "Reader summary"]:
        body_style = ParagraphStyle(
            "PaperAppendixTableCell",
            parent=cell_style,
            fontSize=6.6,
            leading=7.6,
        )
        head_style = ParagraphStyle(
            "PaperAppendixTableHeader",
            parent=body_style,
            fontName="Times-Bold",
        )
    data = []
    for row_index, row in enumerate(normalized):
        style = head_style if row_index == 0 else body_style
        data.append([Paragraph(inline(cell), style) for cell in row])
    table = Table(data, colWidths=col_widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#9a9a9a")),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8e8e8")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#fbfbfb")]),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    return table


def table_column_widths(header: list[str], width: float) -> list[float]:
    weights_by_header = {
        ("Step", "Operation"): [0.16, 0.84],
        ("Claim ID", "Tier", "Reader summary"): [0.10, 0.10, 0.80],
        ("Result / Artifact", "Interaction-derived?", "Source-informed?", "Official status"): [
            0.25,
            0.20,
            0.30,
            0.25,
        ],
        ("Result / Artifact", "Kaggle linkage", "Allowed paper claim"): [0.25, 0.24, 0.51],
        ("Game", "Ontology Characterized", "Substrate Status", "Capability Status", "Claim Boundary"): [
            0.10,
            0.25,
            0.25,
            0.23,
            0.17,
        ],
    }
    weights = weights_by_header.get(tuple(header))
    if weights and len(weights) == len(header):
        return [width * value for value in weights]
    return [width / len(header)] * len(header)


def inline(text: str) -> str:
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"\[@([^\]]+)\]", lambda m: "[" + m.group(1).replace("@", "") + "]", text)
    text = re.sub(r"`([^`]+)`", code_span, text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    return text


def code_span(match: re.Match[str]) -> str:
    value = match.group(1)
    if re.fullmatch(r"[0-9]+(?:[./][0-9]+)*", value) or value in {"ls20", "tr87", "cn04"}:
        return value
    if value.startswith("ACTION"):
        return value
    return f'<font name="Courier">{value}</font>'


def pdf_page_count(path: Path) -> int:
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise SystemExit(
            "pypdf is required for PDF page-count verification. "
            "Use the bundled workspace Python or install pypdf."
        ) from exc
    return len(PdfReader(str(path)).pages)


def build_metadata(
    *,
    manuscript: str,
    reader_text: str,
    used_claims: list[str],
    repo_paths: list[str],
    page_count: int,
    repo_url: str,
    kaggle_url: str,
    reader_md: Path,
    pdf_path: Path,
) -> dict:
    citation_keys = sorted(set(re.findall(r"\[@([^\]]+)\]", reader_text)))
    split_keys = sorted(
        {
            part.strip().lstrip("@")
            for marker in citation_keys
            for part in marker.split(";")
        }
    )
    checks = {
        "reader_markdown_has_no_absolute_users_paths": "/Users/" not in reader_text,
        "reader_markdown_has_no_internal_frontmatter_flags": not any(
            flag in reader_text for flag in INTERNAL_FRONTMATTER_FLAGS
        ),
        "pdf_generated_nonempty": pdf_path.exists() and pdf_path.stat().st_size > 0,
        "source_manuscript_preserved": MANUSCRIPT.read_text() == manuscript,
        "required_reference_keys_present": split_keys == sorted(REFERENCE_KEYS),
        "non_claims_preserved": all(
            phrase in reader_text
            for phrase in [
                "not a general ARC-AGI-3 agent",
                "This is not a high-score leaderboard paper",
                "Kaggle public score `0.0`",
            ]
        ),
    }
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_manuscript": display_path(MANUSCRIPT),
        "source_sha256": sha256(MANUSCRIPT),
        "reader_markdown": display_path(reader_md),
        "pdf_path": display_path(pdf_path),
        "pdf_size_bytes": pdf_path.stat().st_size if pdf_path.exists() else 0,
        "page_count": page_count,
        "claim_id_handling": "in_body_refs_converted_to_appendix_a_claim_index",
        "provenance_handling": "repo_relative_paths_collected_in_data_and_reproducibility_availability",
        "repo_url": repo_url,
        "kaggle_notebook_url": kaggle_url,
        "toolchain": {
            "pandoc": shutil.which("pandoc"),
            "pdflatex": shutil.which("pdflatex"),
            "xelatex": shutil.which("xelatex"),
            "lualatex": shutil.which("lualatex"),
            "reportlab": package_version("reportlab"),
            "pypdf": package_version("pypdf"),
        },
        "citation_keys": split_keys,
        "used_claim_ids": used_claims,
        "repo_relative_paths_collected": repo_paths,
        "checks": checks,
    }


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def package_version(name: str) -> str | None:
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return None


if __name__ == "__main__":
    main()
