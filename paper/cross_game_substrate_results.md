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

# Cross-Game Substrate Results

This is a paper-lane synthesis over existing artifacts. It does not add an
official run, a Kaggle/private-eval claim, a third-game claim, or a general
ARC-AGI-3 agent claim.

## Result Summary

The diagnostic and object-substrate method transferred from `ls20` to `tr87`,
but the game ontology did not.

`ls20` capability used an object state with position, shape, color, and
rotation. `run_005` completed level 1 with score `3.571428571428571`, `1`
level completed, `13` actions, and complete provenance in
`artifacts/object_substrate_v0/run_005_object_aware_wall_fix/receipt.json`.

`tr87` capability used selector index and sequence-rule state. `tr87_run_001`
completed level 1 with score `4.761904761904762`, `1` level completed, `14`
actions, zero prediction mismatches, and complete provenance in
`artifacts/object_substrate_v0/tr87_run_001_object_aware/receipt.json`.

The comparison supports a scoped paper claim: the development method
generalized across two structurally different games, while each game's
perception, action-effect, and target ontology remained game-specific.

## Layer Transferability Map

| Layer | Transfer Status | Evidence |
|---|---|---|
| Diagnostic receipts | transferred | Both games produced official-runner receipts and trace sidecars. |
| Frame-shape dispatch | transferred unchanged | Gamma2a classified `frame_bundle_dispatch` as `transferable_unchanged` in `artifacts/object_substrate_v0/gamma2a_cross_game_substrate_report/cross_game_substrate_report.json`. |
| Actor/perception ontology | did not transfer | Gamma2a classified ls20 actor extraction as `fails` on tr87; gamma2b then built `Tr87ActorState` and achieved `81/81` extraction coverage. |
| Action-effect ontology | did not transfer | ls20 effects were movement/rotation over `ActorState`; tr87 effects were `selector_position_change` and `sequence_state_change` with `uses_motion_delta_representation: false`. |
| Target ontology | did not transfer | ls20 target matching used position/shape/color/rotation equality; tr87 target extraction found `sequence_rule_matching` and `bsqsshqpox_sequence_rule_validation`. |
| Wall/geometry substrate | source-dependent per game | Gamma2a classified wall geometry as `source_dependent_per_game`. |
| Planner discipline | transferred | Both capability runs used precomputed substrate-derived plans, local verification before official execution, and halt-on-mismatch receipts. |

## Evidence Chain

1. Gamma2a transfer audit:
   `artifacts/object_substrate_v0/gamma2a_cross_game_substrate_report/cross_game_substrate_report.json`
   recorded `method_transfers_ontology_doesnt`.
2. Gamma2b tr87 perception:
   `artifacts/object_substrate_v0/tr87_perception/perception_audit.json`
   recorded `81/81` well-formed tr87 actor states and target evidence for
   sequence-rule matching.
3. Gamma2c tr87 action effects:
   `artifacts/object_substrate_v0/tr87_action_effect_model/action_effect_model.json`
   recorded `80` transitions, two tr87 effect categories, and no motion-delta
   representation.
4. Gamma2c.1 selector probe:
   `artifacts/object_substrate_v0/tr87_selector_probe/extended_action_effect_model.json`
   recorded `20/20` action-state coverage and source consistency `1.0`.
5. Gamma2d planner run:
   `artifacts/object_substrate_v0/tr87_run_001_object_aware/receipt.json`
   recorded one official tr87 level completion with zero prediction mismatches.

## Paper Use

This section should become the Results subsection that supports Universality
and Theory:

- Universality: the method reached capability in a second game.
- Theory: the result explains why a shared ontology would have been wrong.
- Progress: the coverage-gated sequence from gamma2c to gamma2c.1 to gamma2d
  is a concrete recipe for avoiding unsupported planner attempts.

## Non-Claims

- No Kaggle/private-eval claim is made here.
- No third-game claim is made here.
- No general extractor API is claimed.
- No all-level completion claim is made for either game.
