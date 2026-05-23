# ARC-AGI-3 Substrate Discovery Paper Release Package

Generated: 2026-05-23T01:21:04.984718+00:00

This package is the clean public-release surface for the paper
**Failure-Driven Substrate Discovery for ARC-AGI-3**. It is prepared for the
fresh public repository at `https://github.com/Haserjian/arc3-substrate-discovery-paper` without private git history.

## Claim Boundary

- Linked Kaggle public score: `0.0`
- Public-scorecard capability: `ls20` and `tr87` level 1
- Method characterization: `ls20`, `tr87`, and `cn04`
- No private-eval capability claim
- No general ARC-AGI-3 solver claim
- No autonomous substrate discovery claim
- No all-level capability claim

## What This Repository Is

This is a static **artifact and evidence release**, not a build-from-source
project. It contains the paper, the linked Kaggle notebook, and the receipts
and summaries that back the paper's claims. The private development repository
that generated these artifacts is not included.

- `paper/` — the reader-clean manuscript (`submission_manuscript.md`), the built
  PDF (`submission_candidate.pdf`), its build metadata, and the claim-support
  docs.
- `kaggle/` — the submitted notebook and its agent, plus the Kaggle
  submission/readiness records for the linked entry.
- `artifacts/` and `docs/` — the receipts, audits, and summaries cited by the
  paper.

### Provenance paths are references, not bundled files

Receipts and the claim inventory cite evidence by repo-relative path. Some of
those paths — for example `tests/...` test names and source-oracle paths under
`arc3_agent/environment_files/...` — point into the private development
repository where the work was produced. They are provenance references that
identify what backs each claim; they are not missing files in this release.

## Intentional Exclusions

The following are deliberately not part of this artifact release:

- The private draft source (`docs/paper/manuscript_v1.md`) and the build /
  preflight tooling that assembled this release. The published PDF and
  reader-clean manuscript under `paper/` are the canonical reader artifacts.
- `docs/paper/kaggle_linkage_plan.md`, a historical planning document. Current
  Kaggle linkage evidence lives in
  `kaggle/submission_record/submission_record.json`.
- The original private repository git history.

## Reading the Evidence

- Read the paper: `paper/submission_candidate.pdf` (or
  `paper/submission_manuscript.md`).
- Check the linked Kaggle result:
  `kaggle/submission_record/submission_record.json` (submitted, succeeded,
  Kaggle public score `0.0`).
- Trace any claim: `paper/claim_inventory.md` maps each claim ID to its backing
  receipts under `artifacts/`.
