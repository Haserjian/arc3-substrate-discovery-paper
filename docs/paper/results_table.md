---
paper_status: draft
submitted: false
peer_reviewed: false
kaggle_score: 0.0
kaggle_submission_status: submitted_succeeded
linked_kaggle_score: 0.0
accuracy_claim_status: linked_kaggle_score_recorded_public_scorecards_separate
public_scorecard_evidence:
  - ls20_run005_score_3.571428571428571_levels_1
  - tr87_run001_score_4.761904761904762_levels_1
licensing_target: CC0_or_MIT-0_per_arc_prize_2026
last_checked: 2026-05-22
---

# Results Table

This table separates official score evidence from methodology and gap evidence.
It is not a private-eval capability claim.

| Run | Game | Purpose | Score | Levels Completed | Actions | Official / Local | Claim Boundary | Artifact |
|---|---|---:|---:|---:|---:|---|---|---|
| run_003_source_derived | ls20 | Source-derived level-1 transfer check | 3.571428571428571 | 1 | 13 | official | Source-derived capability, not substrate planning | `artifacts/planner_v0/run_003_source_derived/receipt.json` |
| run_005_object_aware_wall_fix | ls20 | Substrate-derived level-1 planner after wall-geometry fix | 3.571428571428571 | 1 | 13 | official | Object-aware planning for level 1 only | `artifacts/object_substrate_v0/run_005_object_aware_wall_fix/receipt.json` |
| run_008_grayscale_bundle_fix | ls20 | Multilevel transition/bundle repair attempt | 3.571428571428571 | 1 | 35 | official | Productive failure; level-2 architecture-review gap | `artifacts/object_substrate_v0/run_008_grayscale_bundle_fix/receipt.json` |
| level2_source_mechanic_review | ls20 | Analysis-only source mechanic review | n/a | n/a | n/a | local analysis | Emitted `architecture_review_required`, not run_009 authorization | `artifacts/object_substrate_v0/run_008_grayscale_bundle_fix/level2_source_mechanic_review/next_decision.json` |
| tr87_selector_probe | tr87 | Coverage probe for all `(action, selector_index)` pairs | 0.0 | 0 | 20 | official | Coverage completion, not capability | `artifacts/object_substrate_v0/tr87_selector_probe/receipt.json` |
| tr87_run_001_object_aware | tr87 | Substrate-derived selector/sequence planner | 4.761904761904762 | 1 | 14 | official | Cross-game level-1 capability, not all-level tr87 solution | `artifacts/object_substrate_v0/tr87_run_001_object_aware/receipt.json` |
| gamma3a_third_game_substrate_audit | cn04 | Third ontology characterization | n/a | n/a | n/a | local analysis | Method-transfer evidence only; no planner, no official run, no cn04 capability claim | `artifacts/object_substrate_v0/gamma3a_third_game_substrate_audit/transferability_map_vs_ls20_tr87.json` |
| kaggle_submission_v1 | mixed/private rerun | Linked Kaggle submission for Paper Prize eligibility | 0.0 | n/a | n/a | Kaggle | Linked Accuracy ledger score, not a private-eval capability claim | `artifacts/kaggle_submission_preflight/kaggle_submission_record/submission_record.json` |

## Score Interpretation Boundary

ARC-AGI-3 scoring is completion- and efficiency-based. The official scores
above come from public scorecards. The linked Kaggle submission now exists and
has public score `0.0`; it should be reported as the Kaggle Accuracy ledger,
not merged with the public scorecard capability ledger.

Internal reasoning, local verification, source inspection, and coverage probes
support the methodology claims. They do not count as environment actions unless
they alter the game state, and they do not themselves create Kaggle-linked
Accuracy evidence.

## Non-Claims

- No private-eval score is claimed.
- The linked Kaggle public score is `0.0`; no positive Kaggle leaderboard
  performance claim is made.
- No all-level completion claim is made.
- We make no general ARC-AGI-3 agent claim.
