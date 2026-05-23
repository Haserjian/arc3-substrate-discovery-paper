# ARC-AGI-3 Substrate Discovery Paper Release Package

Generated: 2026-05-23T01:07:38.179986+00:00

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
