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
last_checked: 2026-05-22
---

# Known Gaps

Every gap is tagged with one cost class:

- `cheap`: analysis, documentation, or local-only work over existing artifacts.
- `official-run`: requires a new official-runner or Kaggle-style execution.
- `new-game`: requires adding another ARC-AGI-3 game to the diagnostic set.

## G01 - Linked Kaggle Score Is 0.0

- cost_class: cheap
- paper_impact: High
- affects: Accuracy, claim framing
- current_state: `kaggle_submission_status` is `submitted_succeeded`, but the linked Kaggle public score is `0.0`.
- evidence: `artifacts/kaggle_submission_preflight/kaggle_submission_record/submission_record.json`
- closing_slice: No immediate run. Manuscript v1 must frame the `0.0` linked Kaggle score separately from public scorecard capability evidence.

## G02 - Kaggle Accuracy Remains 0.0 And Official Capability Is Thin

- cost_class: official-run
- paper_impact: High
- affects: Accuracy
- current_state: The paper has scoped official-runner completions in `ls20` and `tr87`, but the linked Kaggle score remains `0.0` and only level 1 is solved in each game.
- evidence: `artifacts/object_substrate_v0/run_005_object_aware_wall_fix/receipt.json`, `artifacts/object_substrate_v0/tr87_run_001_object_aware/receipt.json`, `artifacts/kaggle_submission_preflight/kaggle_submission_record/submission_record.json`
- closing_slice: Do not open another substrate slice by default. Revisit tr87 later levels, ls20 architecture work, or cn04 capability only after final-paper polish if the schedule explicitly supports it.

## G03 - Prior Work Still Needs Manuscript-Grade Integration

- cost_class: cheap
- paper_impact: High
- affects: Novelty, Progress
- current_state: `prior_work_search.md` names direct comparisons, but manuscript v1 must integrate them into a coherent Related Work argument.
- evidence: `docs/paper/prior_work_search.md`
- closing_slice: Use the reviewer map to position against executable world models, graph exploration, and map-then-act systems without claiming world-model novelty.

## G04 - ls20 Level 2 Requires Architecture Review

- cost_class: cheap
- paper_impact: High
- affects: Accuracy, Theory, Progress
- current_state: The level-2 source mechanic review found a source-visible dynamic mechanic, but it failed the bounded-primitive gate and emitted `architecture_review_required`.
- evidence: `artifacts/object_substrate_v0/run_008_grayscale_bundle_fix/level2_source_mechanic_review/next_decision.json`
- closing_slice: Do not run `run_009` from momentum. Either design a dynamic event-state planner locally or leave `ls20` level 2 as the paper's architecture-review gap.

## G05 - Universality Capability Uses Two Games; Method Audit Uses Three

- cost_class: new-game
- paper_impact: High
- affects: Universality, Novelty
- current_state: The method has official capability evidence in `ls20` and `tr87`; gamma3a adds a third ontology audit for `cn04` without a planner or official run.
- evidence: `docs/paper/cross_game_substrate_results.md`, `artifacts/object_substrate_v0/gamma2a_cross_game_substrate_report/cross_game_substrate_report.json`, `artifacts/object_substrate_v0/gamma3a_third_game_substrate_audit/transferability_map_vs_ls20_tr87.json`, `artifacts/object_substrate_v0/gamma3a_third_game_substrate_audit/gamma3b_decision.json`
- closing_slice: Treat gamma3a as sufficient for method-transfer Universality unless a later schedule review explicitly authorizes a bounded `cn04` capability slice.

## G06 - Parameterized Cross-Game Extractor Still Not Implemented

- cost_class: cheap
- paper_impact: Medium
- affects: Theory, Universality
- current_state: `ls20`, `tr87`, and `cn04` now show three different ontology shapes. That supports the paper's per-game substrate argument but does not yet justify or implement a common extractor framework.
- evidence: `docs/object_substrate_v0/tr87_perception_layer.md`, `docs/paper/cross_game_substrate_results.md`, `docs/object_substrate_v0/gamma3a_third_game_substrate_audit.md`
- closing_slice: In final polish, decide whether to describe parameterization as future work or keep the paper centered on per-game substrate discovery.

## G07 - Source-Informed Shortcuts Need Competition-Safe Counterparts

- cost_class: cheap
- paper_impact: Medium
- affects: Completeness, Universality, eligibility trail
- current_state: `ls20` wall geometry and tr87 target semantics are source-informed local-mode artifacts. They are valid research evidence but not sufficient for a private-eval-style generality claim.
- evidence: `artifacts/object_substrate_v0/run_005_object_aware_wall_fix/receipt.json`, `artifacts/object_substrate_v0/tr87_perception/target_spec.json`
- closing_slice: Document which pieces are source-informed and sketch frame-derived or metadata-safe alternatives before any broad competition framing.

## G08 - Action Attribution In Early Diagnostic Traces Is Medium Confidence

- cost_class: cheap
- paper_impact: Medium
- affects: Theory, Completeness
- current_state: Early official recordings still use stdout action-count attribution for diagnostic traces, not direct high-confidence per-row recording action labels.
- evidence: `artifacts/official_agent_smoke/probe_region_semantics_trace.json`, `artifacts/official_agent_smoke/tr87_region_semantics_trace.json`
- closing_slice: Audit official recording action fields and runner stdout alignment; add a higher-confidence action-id path if available.

## G09 - tr87 Later Levels Are Untested

- cost_class: official-run
- paper_impact: Medium
- affects: Accuracy, Universality
- current_state: `tr87_run_001` completed level 1 and stopped. No tr87 level 2+ planner evidence exists.
- evidence: `artifacts/object_substrate_v0/tr87_run_001_object_aware/receipt.json`
- closing_slice: Only after final-paper polish, decide whether a tr87 multilevel slice is worth more than shipping the current evidence.

## G10 - Final Public Release SHA Needs Finalization

- cost_class: cheap
- paper_impact: Medium
- affects: Completeness, eligibility trail
- current_state: The submitted package has package-level MIT-0 metadata and Kaggle submission records, but the final public repository release SHA is not yet recorded in paper docs.
- evidence: `artifacts/kaggle_submission_preflight/kaggle_submission_record/submission_record.json`, `docs/paper/submission_readiness.md`
- closing_slice: Add final public-release SHA checklist before paper submission.

## Top Three By Paper Impact

1. G01 - linked Kaggle score is 0.0 and must be framed correctly.
2. G03 - prior work needs manuscript-grade integration.
3. G05 - Universality capability uses two games while method audit now uses three.

## Non-Claims

- These gaps do not block an internal full draft.
- These gaps do block any positive Kaggle/private-eval capability claim.
- These gaps do not justify all-level or third-game capability claims.
- These gaps do not erase the scoped `ls20` and `tr87` official-runner level-1 completions.
