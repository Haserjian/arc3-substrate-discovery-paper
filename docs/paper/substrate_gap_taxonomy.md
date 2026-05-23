---
paper_status: outline_only
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
last_checked: 2026-05-21
---

# Substrate Gap Taxonomy

This is a paper-lane synthesis over existing artifacts. It is not a submitted
paper section, not peer reviewed, not a Kaggle/private-eval claim, and not a
general ARC-AGI-3 agent claim.

## Taxonomy

The current artifact chain supports two operational gap classes.

### Frame-Format Gaps

Frame-format gaps occur when the runner emits a frame or bundle shape that the
extractor handles incorrectly, even though the underlying game mechanic remains
within the current planner ontology.

Observed examples:

- `run_006` exposed level-transition bundle semantics: the next level's start
  state appeared in the last subframe of a multi-frame bundle.
- `run_007` exposed grayscale bundle shape handling: transition bundles could
  appear as `[N,64,64]`, not only `[N,1,64,64]`.
- `run_008` showed the defensive shape dispatch could handle both
  single-frame and grayscale-bundle conventions in
  `artifacts/object_substrate_v0/run_008_grayscale_bundle_fix/receipt.json`.

Working characterization:

- Usually bounded.
- Usually confirmed from receipts plus source/frame inspection.
- A small substrate extension can often repair the immediate mismatch.
- Repair still requires a new official run before capability claims change.

### Game-Mechanic Gaps

Game-mechanic gaps occur when the current state/action model lacks a real game
mechanic needed for planning, so better frame selection alone cannot produce a
valid path.

Observed example:

- The `ls20` level-2 source mechanic review found dynamic trigger-bound sprite
  automata and emitted `architecture_review_required` in
  `artifacts/object_substrate_v0/run_008_grayscale_bundle_fix/level2_source_mechanic_review/next_decision.json`.

Working characterization:

- Potentially unbounded.
- May require a new planning architecture, dynamic event-state modeling, or a
  local event graph rather than another frame-handler patch.
- Should block immediate official reruns unless a bounded primitive passes the
  explicit gate.

## Why The Distinction Matters

The method's discipline is not "patch until it works." It is:

1. Name the mismatch.
2. Classify the gap.
3. Decide whether the gap is bounded enough to justify a repair.
4. Locally verify before any official attempt.
5. Stop when a gap becomes architectural.

This is why the chain pivoted from `ls20` to `tr87`: after `run_008`, the
level-2 source review did not authorize `run_009`; it recommended
cross-game work with architecture-review notes carried forward.

## Cross-Game Implication

`tr87` gave a contrasting positive case. Its ontology was different from
`ls20`, but once tr87-specific perception and action effects were built, the
coverage-gated planner completed level 1 officially. That contrast is the
strongest current evidence that the method transfers even when the ontology
does not.

## Non-Claims

- This taxonomy is not claimed exhaustive.
- This taxonomy does not prove third-game transfer.
- This taxonomy does not solve `ls20` level 2.
- This taxonomy does not imply that every game-mechanic gap is unbounded.
