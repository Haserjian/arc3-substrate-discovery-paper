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

# Claim Inventory

Allowed tiers: `OBSERVED`, `REFUTED`, `UNKNOWN`.

Allowed evidence strengths: `direct_receipt`, `derived_analysis`,
`cross_artifact_comparison`, `interpretive_summary`.

## Tier Counts

- OBSERVED: 31
- REFUTED: 7
- UNKNOWN: 2

## Claims

### C01 - Kaggle linkage submission succeeded with Kaggle public score 0.0

- tier: OBSERVED
- evidence_strength: direct_receipt
- claim: The ARC-AGI-3 Kaggle linkage submission succeeded and recorded Kaggle public score `0.0`.
- artifacts:
  - artifacts/kaggle_submission_preflight/kaggle_submission_record/submission_record.json
  - artifacts/kaggle_submission_preflight/kaggle_submission_record/notebook_version_commit_record.json
  - artifacts/kaggle_submission_preflight/kaggle_runtime_verification/readiness_verdict.json
- tests:
  - tests/test_kaggle_runtime_verification.py
  - tests/test_paper_manuscript_docs.py
- non_claim_siblings:
  - The linked Kaggle score is `0.0`, not a positive leaderboard result.
  - Public scorecard evidence remains separate from Kaggle leaderboard evidence.
  - No private-eval capability claim exists.

### C02 - ls20 official-runner diagnostic trace scored 0.0

- tier: OBSERVED
- evidence_strength: direct_receipt
- claim: The `ls20` official-runner diagnostic trace scored `0.0`, completed `0` levels, and used `81` actions.
- artifacts:
  - artifacts/official_agent_smoke/official_runner_probe_attempt_receipt.json
- tests:
  - tests/test_receipt_guard_agent.py
- non_claim_siblings:
  - This is not a Kaggle leaderboard score.
  - This is not evidence of ARC-AGI-3 solution capability.

### C03 - ls20 rotating probe produced broad state novelty without progress

- tier: OBSERVED
- evidence_strength: derived_analysis
- claim: The `ls20` rotating probe produced `81` novel states and `0` completed levels.
- artifacts:
  - artifacts/official_agent_smoke/probe_action_effect_trace.json
  - artifacts/official_agent_smoke/official_runner_probe_attempt_receipt.json
- tests:
  - tests/test_action_effect_trace.py
- non_claim_siblings:
  - State novelty is not level progress.
  - Exploration evidence is not goal-reaching evidence.

### C04 - ls20 has four cardinal largest-region motion correlations

- tier: OBSERVED
- evidence_strength: derived_analysis
- claim: `ls20` produced cardinal largest-region motion correlations for ACTION1/ACTION2/ACTION3/ACTION4 under medium-confidence action attribution.
- artifacts:
  - artifacts/official_agent_smoke/probe_region_semantics_trace.json
  - artifacts/official_agent_smoke/hypothesis_bank_seed.json
- tests:
  - tests/test_region_delta_semantics.py
  - tests/test_hypothesis_bank_seed.py
- non_claim_siblings:
  - Largest-region motion is not typed object identity.
  - Cardinal mapping is scoped to this `ls20` trace.

### C05 - tested replay prefix was deterministic

- tier: OBSERVED
- evidence_strength: derived_analysis
- claim: The tested fixed action prefix from reset matched `8/8` paired replay rows.
- artifacts:
  - artifacts/official_agent_smoke/scripted_determinism_report.json
  - artifacts/official_agent_smoke/hypothesis_bank_seed.json
- tests:
  - tests/test_determinism_probe_compare.py
  - tests/test_hypothesis_bank_seed.py
- non_claim_siblings:
  - This is not a global determinism proof.
  - This covers only the tested prefix.

### C06 - exact state-hash inverse assumption was refuted

- tier: REFUTED
- evidence_strength: derived_analysis
- claim: The hypothesis that tested direction pairs return to the exact before-frame state hash is refuted by `0/4` returns.
- artifacts:
  - artifacts/official_agent_smoke/scripted_determinism_report.json
  - artifacts/official_agent_smoke/inverse_failure_mechanism_report.json
  - artifacts/official_agent_smoke/hypothesis_bank_seed.json
- tests:
  - tests/test_determinism_probe_compare.py
  - tests/test_hypothesis_bank_seed.py
- non_claim_siblings:
  - Do not claim all motion is irreversible.
  - Some failures are localized hash drift, not necessarily position non-return.

### C07 - clean position-level inverse assumption was refuted for tested pairs

- tier: REFUTED
- evidence_strength: derived_analysis
- claim: The clean position-level inverse hypothesis is refuted for the tested pair with position-level non-return evidence.
- artifacts:
  - artifacts/official_agent_smoke/inverse_failure_mechanism_report.json
  - artifacts/official_agent_smoke/hypothesis_bank_seed.json
- tests:
  - tests/test_determinism_probe_compare.py
  - tests/test_hypothesis_bank_seed.py
- non_claim_siblings:
  - This is not a complete transition model.
  - Localized hash-drift cases remain ambiguous.

### C08 - ls20 frame shape is not stable across all rows

- tier: OBSERVED
- evidence_strength: derived_analysis
- claim: Rows `42/43` in `ls20` show frame-shape changes `[1,64,64] -> [6,64,64]` and `[6,64,64] -> [1,64,64]`.
- artifacts:
  - artifacts/official_agent_smoke/anomaly_catalog.json
  - artifacts/official_agent_smoke/hypothesis_bank_seed.json
- tests:
  - tests/test_anomaly_catalog.py
  - tests/test_hypothesis_bank_seed.py
- non_claim_siblings:
  - Rows `42/43` are not claimed as goals.
  - Six-channel frames are not claimed as success, checkpoint, transition, or overlay.

### C09 - ls20 frame-shape semantic interpretation remains unknown

- tier: UNKNOWN
- evidence_strength: interpretive_summary
- claim: The best current hypothesis is that rows `42/43` may reflect a structural/render-phase event, but the semantic label is unknown.
- artifacts:
  - artifacts/official_agent_smoke/anomaly_catalog.json
  - docs/anomaly_catalog.md
- tests:
  - tests/test_anomaly_catalog.py
- non_claim_siblings:
  - Do not call the event a goal signal.
  - Do not call the event a proven overlay.

### C10 - tr87 official-runner diagnostic trace scored 0.0

- tier: OBSERVED
- evidence_strength: direct_receipt
- claim: The `tr87` official-runner diagnostic trace scored `0.0`, completed `0` levels, and used `81` actions.
- artifacts:
  - artifacts/official_agent_smoke/tr87_probe_receipt.json
- tests:
  - tests/test_receipt_guard_agent.py
- non_claim_siblings:
  - This is not a Kaggle leaderboard score.
  - This is not evidence of ARC-AGI-3 solution capability.

### C11 - tr87 ACTION1/ACTION2 show scoped local displacement

- tier: OBSERVED
- evidence_strength: derived_analysis
- claim: `tr87` ACTION1/ACTION2 rows show scoped local displacement evidence under the largest-region heuristic.
- artifacts:
  - artifacts/official_agent_smoke/tr87_region_semantics_trace.json
  - artifacts/official_agent_smoke/tr87_anomaly_classification.json
  - artifacts/official_agent_smoke/tr87_hypothesis_bank_seed.json
- tests:
  - tests/test_region_delta_semantics.py
  - tests/test_tr87_anomaly_classification.py
- non_claim_siblings:
  - Do not claim a full tr87 motion ontology.
  - Do not claim the mapping is universal across games.

### C12 - tr87 ACTION3/ACTION4 are localized non-motion/contact-like candidates

- tier: OBSERVED
- evidence_strength: derived_analysis
- claim: `tr87` ACTION3/ACTION4 rows classify as localized non-motion/contact-like candidates, not motion rows.
- artifacts:
  - artifacts/official_agent_smoke/tr87_anomaly_catalog.json
  - artifacts/official_agent_smoke/tr87_anomaly_classification.json
- tests:
  - tests/test_anomaly_catalog.py
  - tests/test_tr87_anomaly_classification.py
- non_claim_siblings:
  - Say contact-like candidates, not proven contact events.
  - The classifier does not detect goals.

### C13 - tr87 uniform all-action motion ontology is refuted

- tier: REFUTED
- evidence_strength: derived_analysis
- claim: The hypothesis that all tr87 probe actions are explained by one largest-region motion ontology is refuted.
- artifacts:
  - artifacts/official_agent_smoke/tr87_anomaly_classification.json
  - artifacts/official_agent_smoke/tr87_hypothesis_bank_seed.json
- tests:
  - tests/test_tr87_anomaly_classification.py
- non_claim_siblings:
  - This does not refute scoped ACTION1/ACTION2 displacement.
  - This does not prove ACTION3/ACTION4 mechanics.

### C14 - method generalized but ontology did not

- tier: OBSERVED
- evidence_strength: cross_artifact_comparison
- claim: The diagnostic method ran on `ls20` and `tr87`, but the motion ontology did not transfer unchanged.
- artifacts:
  - docs/cross_game_diagnostic_comparison.md
  - artifacts/official_agent_smoke/hypothesis_bank_seed.json
  - artifacts/official_agent_smoke/tr87_hypothesis_bank_seed.json
- tests:
  - tests/test_cross_game_comparison.py
- non_claim_siblings:
  - A hypothesis is not universal unless supported across games.
  - Do not force `tr87` into `ls20` categories.

### C15 - anomaly vocabulary did not generalize unchanged

- tier: OBSERVED
- evidence_strength: cross_artifact_comparison
- claim: `ls20` produced rare frame-shape structural/render-phase anomalies while `tr87` produced frequent localized contact/obstacle candidates.
- artifacts:
  - docs/cross_game_diagnostic_comparison.md
  - artifacts/official_agent_smoke/anomaly_catalog.json
  - artifacts/official_agent_smoke/tr87_anomaly_classification.json
- tests:
  - tests/test_cross_game_comparison.py
  - tests/test_tr87_anomaly_classification.py
- non_claim_siblings:
  - Do not promote contact-like candidates to proven contact events.
  - Do not claim one anomaly ontology covers both games.

### C16 - current traces do not justify goal detection

- tier: REFUTED
- evidence_strength: cross_artifact_comparison
- claim: The claim that current traces justify a goal detector is refuted by zero positive goal examples and no legal goal geometry/spec found in the audited runner surface.
- artifacts:
  - artifacts/official_agent_smoke/anomaly_catalog.json
  - artifacts/official_agent_smoke/tr87_anomaly_catalog.json
  - docs/anomaly_catalog.md
- tests:
  - tests/test_anomaly_catalog.py
- non_claim_siblings:
  - The classifier does not detect goals.
  - The classifier does not predict level completion.

### C17 - positive private/Kaggle capability claims are refuted

- tier: REFUTED
- evidence_strength: direct_receipt
- claim: Current artifacts explicitly refute positive Kaggle leaderboard capability and private-eval capability claims; the Kaggle public score is `0.0`.
- artifacts:
  - artifacts/kaggle_submission_preflight/kaggle_submission_record/submission_record.json
  - kaggle/arc_agi_3_receiptguard/submission_manifest.json
  - docs/kaggle_linkage.md
- tests:
  - tests/test_kaggle_linkage_package.py
  - tests/test_paper_manuscript_docs.py
- non_claim_siblings:
  - A Kaggle submission exists, but it records Kaggle public score `0.0`.
  - Official-runner score evidence is separate from Kaggle leaderboard evidence.

### C18 - planner-v0 official attempt executed with complete provenance and 0.0 score

- tier: OBSERVED
- evidence_strength: direct_receipt
- claim: Planner-v0 executed one official-runner `ls20` attempt with complete per-step provenance, scored `0.0`, and completed `0` levels.
- artifacts:
  - artifacts/planner_v0/run_001/receipt.json
  - artifacts/planner_v0/run_001/steps
- tests:
  - tests/test_receipt_planner_agent.py
  - tests/test_planner_v0_run_001_analysis.py
- non_claim_siblings:
  - This is not a Kaggle/private-eval claim.
  - This is not a winning ARC-AGI-3 solution claim.

### C19 - ls20 phase-transition event recurred near the same action count across probe and planner-v0

- tier: OBSERVED
- evidence_strength: cross_artifact_comparison
- claim: The `ls20` phase-transition event recurred near the same action count across probe and planner-v0, and the first planner phase edge matched the probe phase edge by before/after state hash.
- artifacts:
  - artifacts/planner_v0/run_001/phase_transition_analysis.json
- tests:
  - tests/test_planner_v0_run_001_analysis.py
- non_claim_siblings:
  - This does not prove a goal signal.
  - This does not prove a fixed time-based scheduler.
  - This does not prove score improvement.

### C20 - phase-transition-as-completion evidence is refuted for run_001

- tier: REFUTED
- evidence_strength: derived_analysis
- claim: Run `001` refutes treating the observed phase-transition signal as sufficient evidence of level completion.
- artifacts:
  - artifacts/planner_v0/run_001/receipt.json
  - artifacts/planner_v0/run_001/phase_transition_analysis.json
- tests:
  - tests/test_planner_v0_run_001_analysis.py
- non_claim_siblings:
  - Phase transitions may still be useful observations.
  - Phase transitions are not currently justified as goal detectors.

### C21 - contact-probe substrate live-run planning value remains unknown

- tier: UNKNOWN
- evidence_strength: derived_analysis
- claim: The contact-probe substrate was logged during run `001`, but its live-run planning value remains unknown because every step was an unexplored frontier edge and no contact segment was cited in a per-step receipt.
- artifacts:
  - artifacts/planner_v0/run_001/contact_expectation_comparison.json
- tests:
  - tests/test_planner_v0_run_001_analysis.py
- non_claim_siblings:
  - Contact-like candidates are not proven contact events.
  - Move-until-blocked is not validated as a completion primitive.

### C22 - ls20 run_005 completed level 1 via object-aware planning

- tier: OBSERVED
- evidence_strength: direct_receipt
- claim: `run_005` completed `ls20` level 1 with score `3.571428571428571`, `1` level completed, and `13` actions after local verification passed.
- artifacts:
  - artifacts/object_substrate_v0/run_005_object_aware_wall_fix/receipt.json
  - artifacts/object_substrate_v0/run_005_object_aware_wall_fix/pre_run_plan.json
  - artifacts/object_substrate_v0/run_005_object_aware_wall_fix/run_005_analysis.json
- tests:
  - tests/test_object_substrate_v0_run_005.py
  - tests/test_object_substrate_v0_slice_gamma1a.py
- non_claim_siblings:
  - This is not a Kaggle/private-eval claim.
  - This does not claim multi-level `ls20` capability.

### C23 - ls20 run_005 sequence converged to the source-derived run_003 sequence

- tier: OBSERVED
- evidence_strength: cross_artifact_comparison
- claim: `run_005` planned sequence `[3,3,3,1,1,1,1,4,4,4,1,1,1]` matched the earlier source-derived `run_003` sequence, while `run_005` recorded planner-derived sequence provenance.
- artifacts:
  - artifacts/object_substrate_v0/run_005_object_aware_wall_fix/receipt.json
  - artifacts/planner_v0/run_003_source_derived/receipt.json
  - docs/planner_v0/run_003_source_derived.md
- tests:
  - tests/test_object_substrate_v0_run_005.py
  - tests/test_planner_v0_run_003_source_derived.py
- non_claim_siblings:
  - Matching output sequence is not evidence that the planner imported a source replay.
  - This does not prove uniqueness of the optimal path.

### C24 - ls20 run_008 crossed level 1 but exposed level-2 divergence

- tier: OBSERVED
- evidence_strength: direct_receipt
- claim: `run_008` locally verified levels `[1,2]`, crossed the level-1 transition online, but the official run still completed only `1` level and recorded `official_local_online_divergence`.
- artifacts:
  - artifacts/object_substrate_v0/run_008_grayscale_bundle_fix/receipt.json
  - artifacts/object_substrate_v0/run_008_grayscale_bundle_fix/local_verification.json
  - artifacts/object_substrate_v0/run_008_grayscale_bundle_fix/post_run_diagnosis.json
- tests:
  - tests/test_object_substrate_v0_frame_bundle_handler.py
  - tests/test_object_substrate_v0_slice_gamma1b.py
- non_claim_siblings:
  - This is not a successful multi-level `ls20` claim.
  - The divergence is not treated as a reason to run another official attempt without analysis.

### C25 - ls20 level-2 source review required architecture review

- tier: OBSERVED
- evidence_strength: derived_analysis
- claim: The level-2 source mechanic review emitted `architecture_review_required` because the source-visible dynamic trigger-bound sprite automata failed the bounded-primitive gate.
- artifacts:
  - artifacts/object_substrate_v0/run_008_grayscale_bundle_fix/level2_source_mechanic_review/next_decision.json
  - artifacts/object_substrate_v0/run_008_grayscale_bundle_fix/level2_source_mechanic_review/event_graph_gap_audit.json
  - docs/object_substrate_v0/level2_source_mechanic_review.md
- tests:
  - tests/test_object_substrate_v0_level2_source_mechanic_review.py
- non_claim_siblings:
  - This is not a claim that `ls20` level 2 is impossible.
  - This is not a bounded run_009 authorization.

### C26 - substrate gaps separated into frame-format and game-mechanic categories

- tier: OBSERVED
- evidence_strength: interpretive_summary
- claim: The artifact chain supports a paper taxonomy separating bounded frame-format gaps from larger game-mechanic gaps that may require architecture review.
- artifacts:
  - docs/paper/substrate_gap_taxonomy.md
  - artifacts/object_substrate_v0/level_transition_spec.json
  - artifacts/object_substrate_v0/run_008_grayscale_bundle_fix/level2_source_mechanic_review/next_decision.json
- tests:
  - tests/test_paper_outline_docs.py
  - tests/test_object_substrate_v0_frame_bundle_handler.py
- non_claim_siblings:
  - The taxonomy is a current-project theory claim, not a universal ARC-AGI-3 law.
  - The taxonomy does not solve the open game-mechanic gaps.

### C27 - gamma2a found method transfer with ontology breakage on tr87

- tier: OBSERVED
- evidence_strength: cross_artifact_comparison
- claim: The gamma2a cross-game substrate audit classified the finding as `method_transfers_ontology_doesnt`: frame/bundle and diagnostic layers transferred, while actor, action, target, and mechanic layers required tr87-specific redesign.
- artifacts:
  - artifacts/object_substrate_v0/gamma2a_cross_game_substrate_report/cross_game_substrate_report.json
  - artifacts/object_substrate_v0/gamma2a_cross_game_substrate_report/next_slice_decision.json
  - docs/object_substrate_v0/gamma2a_cross_game_substrate_report.md
- tests:
  - tests/test_object_substrate_v0_gamma2a_cross_game_substrate_report.py
- non_claim_siblings:
  - This does not claim the ls20 ontology works on tr87.
  - This does not claim third-game generality.

### C28 - tr87 perception layer extracted actor state on 81/81 frames

- tier: OBSERVED
- evidence_strength: derived_analysis
- claim: The tr87-specific perception audit produced well-formed `Tr87ActorState` on `81/81` frames with coverage rate `1.0`.
- artifacts:
  - artifacts/object_substrate_v0/tr87_perception/perception_audit.json
  - artifacts/object_substrate_v0/tr87_perception/tr87_source_availability.json
  - docs/object_substrate_v0/tr87_perception_layer.md
- tests:
  - tests/test_object_substrate_v0_tr87_perception.py
- non_claim_siblings:
  - This does not make the ls20 `ActorState` extractor general.
  - This does not by itself prove tr87 planning capability.

### C29 - tr87 target structure is sequence-rule matching

- tier: OBSERVED
- evidence_strength: derived_analysis
- claim: The tr87 target extractor characterized the goal as `sequence_rule_matching` with completion predicate `bsqsshqpox_sequence_rule_validation`.
- artifacts:
  - artifacts/object_substrate_v0/tr87_perception/target_spec.json
  - artifacts/object_substrate_v0/tr87_perception/perception_audit.json
  - docs/object_substrate_v0/tr87_perception_layer.md
- tests:
  - tests/test_object_substrate_v0_tr87_perception.py
- non_claim_siblings:
  - This is not an ls20-style position/shape/color/rotation target.
  - This does not claim target structures generalize to other games.

### C30 - tr87 action effects are selector/sequence effects, not motion deltas

- tier: OBSERVED
- evidence_strength: derived_analysis
- claim: The tr87 action-effect model analyzed `80` transitions and identified `selector_position_change` and `sequence_state_change`, with `uses_motion_delta_representation: false`.
- artifacts:
  - artifacts/object_substrate_v0/tr87_action_effect_model/action_effect_model.json
  - docs/object_substrate_v0/tr87_action_effect_model.md
- tests:
  - tests/test_object_substrate_v0_tr87_action_effect_model.py
- non_claim_siblings:
  - Do not recast tr87 as a grid-motion task.
  - Do not reuse ls20 action-effect dataclasses for tr87 claims.

### C31 - tr87 action-effect source consistency passed on 80/80 transitions

- tier: OBSERVED
- evidence_strength: derived_analysis
- claim: The gamma2c consistency checker reported `80/80` transition checks passed with pass rate `1.0` and mismatch count `0`.
- artifacts:
  - artifacts/object_substrate_v0/tr87_action_effect_model/consistency_check.json
  - artifacts/object_substrate_v0/tr87_action_effect_model/action_effect_model.json
  - docs/object_substrate_v0/tr87_action_effect_model.md
- tests:
  - tests/test_object_substrate_v0_tr87_action_effect_model.py
- non_claim_siblings:
  - Source consistency is not private-eval validation.
  - Source consistency does not remove the need for official-runner receipts.

### C32 - gamma2c correctly blocked planner work on sparse selector coverage

- tier: OBSERVED
- evidence_strength: derived_analysis
- claim: Before the selector probe, gamma2c recorded only `4/20` observed action/state pairs, `16` known gaps, and `ready_for_gamma2d_planner: false`.
- artifacts:
  - artifacts/object_substrate_v0/tr87_action_effect_model/known_gaps.json
  - docs/object_substrate_v0/tr87_action_effect_model.md
- tests:
  - tests/test_object_substrate_v0_tr87_action_effect_model.py
- non_claim_siblings:
  - The sparse model was not treated as sufficient for a planner attempt.
  - This is a substrate-readiness gate, not a capability result.

### C33 - tr87 selector probe closed coverage to 20/20

- tier: OBSERVED
- evidence_strength: direct_receipt
- claim: The targeted selector coverage probe observed `20/20` `(action, selector_index)` pairs, with source consistency pass rate `1.0` and `ready_for_gamma2d_planner: true`.
- artifacts:
  - artifacts/object_substrate_v0/tr87_selector_probe/receipt.json
  - artifacts/object_substrate_v0/tr87_selector_probe/extended_action_effect_model.json
  - docs/object_substrate_v0/tr87_selector_probe.md
- tests:
  - tests/test_object_substrate_v0_tr87_selector_probe.py
- non_claim_siblings:
  - The selector probe was not a planner attempt.
  - Its `0.0` score is not a failure of the later planner.

### C34 - tr87 selector probe produced coverage but no capability score

- tier: OBSERVED
- evidence_strength: direct_receipt
- claim: The selector coverage probe scored `0.0`, completed `0` levels, and took `20` actions while completing its coverage objective.
- artifacts:
  - artifacts/object_substrate_v0/tr87_selector_probe/receipt.json
  - artifacts/object_substrate_v0/tr87_selector_probe/probe_sequence.json
  - artifacts/object_substrate_v0/tr87_selector_probe/pre_run_plan.json
- tests:
  - tests/test_object_substrate_v0_tr87_selector_probe.py
- non_claim_siblings:
  - Coverage closure is not level completion.
  - This receipt should not be counted as a tr87 capability run.

### C35 - tr87 planner locally verified a selector/sequence completion plan

- tier: OBSERVED
- evidence_strength: derived_analysis
- claim: The tr87 local verifier passed a `14`-action plan over selector/sequence state before official execution.
- artifacts:
  - artifacts/object_substrate_v0/tr87_run_001_object_aware/local_verification.json
  - artifacts/object_substrate_v0/tr87_run_001_object_aware/planned_sequence.json
  - artifacts/object_substrate_v0/tr87_run_001_object_aware/pre_run_plan.json
- tests:
  - tests/test_object_substrate_v0_tr87_planner.py
- non_claim_siblings:
  - Local verification alone is not an official score claim.
  - The plan is not a source-copied replay sequence.

### C36 - tr87 run_001 completed level 1 officially

- tier: OBSERVED
- evidence_strength: direct_receipt
- claim: The tr87 object-aware planner official run scored `4.761904761904762`, completed `1` level, took `14` actions, and used planned sequence `[2,2,3,2,2,3,2,3,1,1,1,3,2,2]`.
- artifacts:
  - artifacts/object_substrate_v0/tr87_run_001_object_aware/receipt.json
  - artifacts/object_substrate_v0/tr87_run_001_object_aware/planned_sequence.json
  - docs/object_substrate_v0/tr87_run_001.md
- tests:
  - tests/test_object_substrate_v0_tr87_planner.py
- non_claim_siblings:
  - This is not a Kaggle/private-eval claim.
  - This does not claim all tr87 levels are solved.

### C37 - tr87 run_001 had zero prediction mismatches and complete provenance

- tier: OBSERVED
- evidence_strength: direct_receipt
- claim: The tr87 run_001 receipt reported `prediction_mismatch_count: 0`, no failure modes, and `provenance_complete: true`.
- artifacts:
  - artifacts/object_substrate_v0/tr87_run_001_object_aware/receipt.json
  - artifacts/object_substrate_v0/tr87_run_001_object_aware/steps
- tests:
  - tests/test_object_substrate_v0_tr87_planner.py
- non_claim_siblings:
  - Zero mismatches on level 1 is not a guarantee for later levels.
  - Complete provenance is not the same as broad general capability.

### C38 - cross-game capability exists across two structurally different ontologies

- tier: OBSERVED
- evidence_strength: cross_artifact_comparison
- claim: The object-substrate pipeline produced official level-1 completions for both `ls20` and `tr87`, despite `ls20` using position/shape/color/rotation matching and `tr87` using selector/sequence-rule matching.
- artifacts:
  - artifacts/object_substrate_v0/run_005_object_aware_wall_fix/receipt.json
  - artifacts/object_substrate_v0/tr87_run_001_object_aware/receipt.json
  - docs/paper/cross_game_substrate_results.md
- tests:
  - tests/test_object_substrate_v0_run_005.py
  - tests/test_object_substrate_v0_tr87_planner.py
  - tests/test_paper_outline_docs.py
- non_claim_siblings:
  - Two games are not enough for a universal-agent claim.
  - The shared contribution is the method, not a shared game ontology.

### C39 - third-game ontology characterization exists without third-game capability

- tier: OBSERVED
- evidence_strength: derived_analysis
- claim: Gamma3a characterized `cn04` as a third distinct ontology, click-selected sprite manipulation with movement, rotation/cycling, masking, and marker-completion, while explicitly emitting `audit_only_sufficient` rather than authorizing a planner or official run.
- artifacts:
  - docs/paper/known_gaps.md
  - docs/paper/cross_game_substrate_results.md
  - docs/object_substrate_v0/gamma3a_third_game_substrate_audit.md
  - artifacts/object_substrate_v0/gamma3a_third_game_substrate_audit/game_selection.json
  - artifacts/object_substrate_v0/gamma3a_third_game_substrate_audit/transferability_map_vs_ls20_tr87.json
  - artifacts/object_substrate_v0/gamma3a_third_game_substrate_audit/gamma3b_decision.json
- tests:
  - tests/test_object_substrate_v0_gamma3a_audit.py
  - tests/test_paper_outline_docs.py
  - tests/test_paper_reviewer_map.py
- non_claim_siblings:
  - Do not claim third-game completion.
  - Do not claim third-game official capability.
  - Do not claim a general extractor API from three games.

### C40 - general ARC-AGI-3 and private-eval claims remain refuted

- tier: REFUTED
- evidence_strength: cross_artifact_comparison
- claim: The current evidence refutes broad claims that the project has a general ARC-AGI-3 agent, private-eval capability, or positive Kaggle leaderboard performance.
- artifacts:
  - docs/paper/known_gaps.md
  - artifacts/object_substrate_v0/run_005_object_aware_wall_fix/receipt.json
  - artifacts/object_substrate_v0/tr87_run_001_object_aware/receipt.json
  - artifacts/kaggle_submission_preflight/kaggle_submission_record/submission_record.json
- tests:
  - tests/test_paper_outline_docs.py
  - tests/test_kaggle_linkage_package.py
- non_claim_siblings:
  - Official-runner level completions are real but scoped.
  - Kaggle linkage exists with public score `0.0`, so positive leaderboard and private-eval language remains prohibited.

## Stale Hypothesis Audit

The current `tr87` hypothesis seed contains no ACTION3/ACTION4 motion entries.
It contains scoped ACTION1/ACTION2 motion entries and
`tr87_uniform_motion_ontology_all_actions: REFUTED`.

Artifact:

- `artifacts/official_agent_smoke/tr87_hypothesis_bank_seed.json`
