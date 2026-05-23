---
paper_status: draft
submitted: false
peer_reviewed: false
kaggle_score: 0.0
kaggle_submission_status: submitted_succeeded
linked_kaggle_score: 0.0
accuracy_claim_status: linked_kaggle_score_recorded_public_scorecards_separate
licensing_target: CC0_or_MIT-0_per_arc_prize_2026
---

# Gamma3a Third-Game Substrate Audit

## Method

This slice is an analysis-only substrate-transfer audit for `cn04`. It reads
the public local source oracle at
`arc3_agent/environment_files/cn04/2fe56bfb/cn04.py`
and does not run an official ARC attempt, build a planner, invoke Kaggle, or
claim third-game capability.

## Game Selection

Selected game: `cn04`.

Reason selected: cn04 exposes a click-selected sprite manipulation ontology: ACTION6 selects/deselects sprites, ACTION1-4 move the selected sprite on a 20x20 grid, and ACTION5 rotates or cycles overlapping sprite variants. This is structurally distinct from ls20 motion/target matching and tr87 selector/sequence-rule construction.

Ontology hypothesis: `selected_sprite + sprite_group_variant + rotation + contact-marker-completion`.

Rejected candidates:
[
  {
    "game": "bp35",
    "reason": "compact but less clearly distinct from object-manipulation without deeper source audit",
    "risk": "medium: ontology signal weaker than cn04 from initial static scan"
  },
  {
    "game": "cd82",
    "reason": "visually rich candidate, but source scan did not expose as clean an action ontology within the timebox",
    "risk": "medium: audit likely needs additional trace data"
  },
  {
    "game": "wa30",
    "reason": "initial scan suggested more motion-like mechanics, reducing ontology contrast with ls20",
    "risk": "medium"
  },
  {
    "game": "dc22",
    "reason": "large source surface would exceed the bounded audit before establishing distinctness",
    "risk": "high: 10000+ source lines"
  }
]

## Perception Audit

Result: `third_ontology_characterized:click_selected_sprite_manipulation`.

The observable state variables are:
[
  {
    "citations": [
      "cn04.py:836",
      "cn04.py:888-904"
    ],
    "confidence": "high",
    "evidence": "self.xseexqzst is the selected Sprite and is changed by selection handlers",
    "name": "selected_sprite_identity"
  },
  {
    "citations": [
      "cn04.py:1102-1125"
    ],
    "confidence": "high",
    "evidence": "ACTION1-4 mutate the selected sprite position inside grid bounds",
    "name": "selected_sprite_position"
  },
  {
    "citations": [
      "cn04.py:1089-1097"
    ],
    "confidence": "high",
    "evidence": "ACTION5 rotates singleton selected sprites by 90 degrees",
    "name": "selected_sprite_rotation"
  },
  {
    "citations": [
      "cn04.py:872-879",
      "cn04.py:1075-1081",
      "cn04.py:1133-1157"
    ],
    "confidence": "medium",
    "evidence": "overlapping sprites are grouped and ACTION5/ACTION6 can cycle the visible selection",
    "name": "sprite_group_variant"
  },
  {
    "citations": [
      "cn04.py:946-994",
      "cn04.py:1023-1049"
    ],
    "confidence": "medium",
    "evidence": "source tracks overlapping 8/13 marker cells and rewrites them during rendering and completion checks",
    "name": "contact_marker_coverage"
  }
]

Coverage: `{'source_lines_scanned': 1182, 'levels_scanned': 6, 'sys_click_sprite_definitions': 47, 'observable_state_variable_count': 5, 'empirical_frames_analyzed': 0}`.

## Action-Effect Audit

Result: `source_visible_action_effects_characterized_without_planner`.

Per-action categories:
{
  "motion": [
    "ACTION1",
    "ACTION2",
    "ACTION3",
    "ACTION4"
  ],
  "object_transform": [
    "ACTION5"
  ],
  "reset/failure": [],
  "selection": [
    "ACTION6"
  ],
  "sequence_advance": [],
  "toggle": [
    "ACTION5",
    "ACTION6"
  ],
  "unknown": []
}

## Goal Evidence

Result: `target_goal_evidence_present:contact_marker_completion`.

Target state: `all source-defined contact-marker cells covered/rewritten`.

Completion signal: `self.rqolqpqwo then next_level on following step`.

## Transferability Map

Third ontology summary:
`click-selected sprite manipulation with movement, rotation/cycling, masking, and marker completion`.

Methodology transfer finding:
`method_transfers_across_three_ontologies_while_ontology_remains_game_specific`.

Layer map:
{
  "action-effect ontology": {
    "citations": [
      "cn04.py:1062-1157"
    ],
    "explanation": "ACTION1-4 resemble movement, but effects are conditioned on selected sprite; ACTION5/ACTION6 add transform, cycling, and click selection.",
    "new_substrate_required": "yes",
    "transfers_from_ls20": "partial",
    "transfers_from_tr87": "partial"
  },
  "actor/state ontology": {
    "citations": [
      "cn04.py:1062-1128"
    ],
    "explanation": "Movement exists, but the controlled object is a click-selected sprite rather than a persistent ls20 actor or tr87 selector index.",
    "new_substrate_required": "yes",
    "transfers_from_ls20": "partial",
    "transfers_from_tr87": "no"
  },
  "frame/bundle handling": {
    "citations": [
      "cn04.py:700-798",
      "cn04.py:861-871"
    ],
    "explanation": "Basic frame/bundle discipline transfers, but cn04 adds source-visible 20x20 sprite layouts, masking, and click-selected sprite visual states that need cn04-specific extraction.",
    "new_substrate_required": "yes",
    "transfers_from_ls20": "partial",
    "transfers_from_tr87": "partial"
  },
  "local verification feasibility": {
    "citations": [
      "cn04.py:1051-1131"
    ],
    "explanation": "Source-visible semantics make a verifier plausible, but gamma3a did not build or execute one.",
    "new_substrate_required": "yes",
    "transfers_from_ls20": "partial",
    "transfers_from_tr87": "partial"
  },
  "perception extraction": {
    "citations": [
      "cn04.py:888-904",
      "cn04.py:920-1021"
    ],
    "explanation": "cn04 needs selected-sprite, sprite-group, rotation, and marker-coverage extraction.",
    "new_substrate_required": "yes",
    "transfers_from_ls20": "no",
    "transfers_from_tr87": "no"
  },
  "planner feasibility": {
    "citations": [
      "cn04.py:1062-1088",
      "cn04.py:1133-1157"
    ],
    "explanation": "A planner would need click coordinate actions plus selected-object state; no planner is attempted.",
    "new_substrate_required": "yes",
    "transfers_from_ls20": "partial",
    "transfers_from_tr87": "partial"
  },
  "target/goal ontology": {
    "citations": [
      "cn04.py:946-994",
      "cn04.py:1023-1049"
    ],
    "explanation": "Completion depends on marker coverage/elimination across sprites, not target equality or sequence equality.",
    "new_substrate_required": "yes",
    "transfers_from_ls20": "no",
    "transfers_from_tr87": "no"
  }
}

## Gap Classification

[
  {
    "boundedness": "bounded_but_unimplemented",
    "citations": [
      "cn04.py:888-904",
      "cn04.py:920-1021"
    ],
    "description": "A cn04 extractor must identify selected sprite state, sprite groups, rotation, masking, and contact-marker coverage.",
    "gap_id": "G3A-PERCEPTION",
    "label": "perception-ontology gap"
  },
  {
    "boundedness": "bounded_but_needs_empirical_trace",
    "citations": [
      "cn04.py:1062-1099",
      "cn04.py:1133-1157"
    ],
    "description": "ACTION6 carries click coordinates, while ACTION5 may rotate or cycle variants depending on group state.",
    "gap_id": "G3A-ACTION",
    "label": "action-effect gap"
  },
  {
    "boundedness": "bounded_source_visible",
    "citations": [
      "cn04.py:946-994",
      "cn04.py:1023-1049"
    ],
    "description": "Completion is marker-elimination over sprite overlap geometry and is not captured by ls20 target equality or tr87 sequence equality.",
    "gap_id": "G3A-GOAL",
    "label": "target/goal gap"
  },
  {
    "boundedness": "unimplemented",
    "citations": [
      "cn04.py:1051-1131"
    ],
    "description": "No cn04 local verifier or empirical transition trace exists in gamma3a.",
    "gap_id": "G3A-VERIFIER",
    "label": "local-verifier gap"
  }
]

## Gamma3b Decision

Decision: `audit_only_sufficient`.

Reason: The third ontology is characterized cleanly enough to strengthen R14 as method-transfer evidence, but gamma3a has no empirical cn04 trace, no coordinate-action model, and no local verifier. A capability attempt would be premature.

R14 update recommendation: `strong`.

## Non-Claims

- No official run was attempted.
- No planner was built.
- No third-game capability claim is made.
- No private-eval claim is made.
- No general ARC-AGI-3 solution claim is made.
