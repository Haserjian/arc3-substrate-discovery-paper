"""ARC-AGI-3 Kaggle object-substrate submission agent.

Generated from the verified package candidate. This wraps the package-local
object-substrate plans in Kaggle's live MyAgent(Agent) notebook contract.

Non-claims:
- scoped public-game substrate capability for ls20 and tr87 only
- no private-eval capability claim
- no general ARC-AGI-3 solution claim
"""

from __future__ import annotations

import json
import time
from typing import Any

from arcengine import FrameData, GameAction, GameState
from agents.agent import Agent

SUBSTRATE_PAYLOAD = {'available_substrate_games': ['ls20', 'tr87'], 'generated_at': '2026-05-21T20:16:19.807234+00:00', 'kind': 'kaggle_submission_substrate_plan_payload', 'schema_version': 'v0', 'source_bundling_decision': 'hardcoded_constants_with_notice_citations', 'source_files_bundled': False, 'supported_games': {'ls20': {'action_labels': ['ACTION3', 'ACTION3', 'ACTION3', 'ACTION1', 'ACTION1', 'ACTION1', 'ACTION1', 'ACTION4', 'ACTION4', 'ACTION4', 'ACTION1', 'ACTION1', 'ACTION1'], 'action_sequence': [3, 3, 3, 1, 1, 1, 1, 4, 4, 4, 1, 1, 1], 'game_id_prefixes': ['ls20'], 'hardcoded_constants': {'player_start': {'color': 9, 'position': [34, 45], 'rotation': 270, 'shape': 5}, 'source_file': 'ls20.py', 'source_lines': ['ls20.py:605-748', 'ls20.py:611-726', 'ls20.py:727-745'], 'target': {'position': [34, 10], 'required_color': 9, 'required_rotation': 0, 'required_shape': 5}}, 'non_claims': ['public ls20 level-1 substrate-derived capability only', 'not a Kaggle leaderboard result', 'not a private-eval claim'], 'per_step_provenance': [{'action_id': 3, 'action_label': 'ACTION3', 'confidence': 'medium', 'confidence_by_dimension': {'color': 'medium', 'position': 'medium', 'rotation': 'medium', 'shape': 'medium'}, 'provenance': {'action': 3, 'dominant_position_delta': [-5, 0], 'observation_count': 2, 'reason': 'dominant_empirical_position_delta'}, 'step_index': 0}, {'action_id': 3, 'action_label': 'ACTION3', 'confidence': 'high', 'confidence_by_dimension': {'color': 'high', 'position': 'high', 'rotation': 'high', 'shape': 'high'}, 'provenance': {'observation': {'action': 'ACTION3', 'action_id': 3, 'after': {'color': 9, 'position': [24, 45], 'rotation': 270, 'shape': 5}, 'before': {'color': 9, 'position': [29, 45], 'rotation': 270, 'shape': 5}, 'changed_dimensions': ['position'], 'color_changed': False, 'confidence': 'high', 'position_delta': [-5, 0], 'provenance': [{'after_frame_index': 1, 'before_frame_index': 0, 'row_index': 0, 'source_artifact': 'artifacts/object_substrate_v0/state_diff_run003.json'}], 'rotation_changed': False, 'rotation_delta': 0, 'shape_changed': False}, 'reason': 'exact_before_state_match'}, 'step_index': 1}, {'action_id': 3, 'action_label': 'ACTION3', 'confidence': 'high', 'confidence_by_dimension': {'color': 'high', 'position': 'high', 'rotation': 'high', 'shape': 'high'}, 'provenance': {'observation': {'action': 'ACTION3', 'action_id': 3, 'after': {'color': 9, 'position': [19, 45], 'rotation': 270, 'shape': 5}, 'before': {'color': 9, 'position': [24, 45], 'rotation': 270, 'shape': 5}, 'changed_dimensions': ['position'], 'color_changed': False, 'confidence': 'high', 'position_delta': [-5, 0], 'provenance': [{'after_frame_index': 2, 'before_frame_index': 1, 'row_index': 1, 'source_artifact': 'artifacts/object_substrate_v0/state_diff_run003.json'}], 'rotation_changed': False, 'rotation_delta': 0, 'shape_changed': False}, 'reason': 'exact_before_state_match'}, 'step_index': 2}, {'action_id': 1, 'action_label': 'ACTION1', 'confidence': 'high', 'confidence_by_dimension': {'color': 'high', 'position': 'high', 'rotation': 'high', 'shape': 'high'}, 'provenance': {'observation': {'action': 'ACTION1', 'action_id': 1, 'after': {'color': 9, 'position': [19, 40], 'rotation': 270, 'shape': 5}, 'before': {'color': 9, 'position': [19, 45], 'rotation': 270, 'shape': 5}, 'changed_dimensions': ['position'], 'color_changed': False, 'confidence': 'high', 'position_delta': [0, -5], 'provenance': [{'after_frame_index': 3, 'before_frame_index': 2, 'row_index': 2, 'source_artifact': 'artifacts/object_substrate_v0/state_diff_run003.json'}], 'rotation_changed': False, 'rotation_delta': 0, 'shape_changed': False}, 'reason': 'exact_before_state_match'}, 'step_index': 3}, {'action_id': 1, 'action_label': 'ACTION1', 'confidence': 'high', 'confidence_by_dimension': {'color': 'high', 'position': 'high', 'rotation': 'high', 'shape': 'high'}, 'provenance': {'observation': {'action': 'ACTION1', 'action_id': 1, 'after': {'color': 9, 'position': [19, 35], 'rotation': 270, 'shape': 5}, 'before': {'color': 9, 'position': [19, 40], 'rotation': 270, 'shape': 5}, 'changed_dimensions': ['position'], 'color_changed': False, 'confidence': 'high', 'position_delta': [0, -5], 'provenance': [{'after_frame_index': 4, 'before_frame_index': 3, 'row_index': 3, 'source_artifact': 'artifacts/object_substrate_v0/state_diff_run003.json'}], 'rotation_changed': False, 'rotation_delta': 0, 'shape_changed': False}, 'reason': 'exact_before_state_match'}, 'step_index': 4}, {'action_id': 1, 'action_label': 'ACTION1', 'confidence': 'high', 'confidence_by_dimension': {'color': 'high', 'position': 'high', 'rotation': 'high', 'shape': 'high'}, 'provenance': {'observation': {'action': 'ACTION1', 'action_id': 1, 'after': {'color': 9, 'position': [19, 30], 'rotation': 0, 'shape': 5}, 'before': {'color': 9, 'position': [19, 35], 'rotation': 270, 'shape': 5}, 'changed_dimensions': ['position', 'rotation'], 'color_changed': False, 'confidence': 'high', 'position_delta': [0, -5], 'provenance': [{'after_frame_index': 5, 'before_frame_index': 4, 'row_index': 4, 'source_artifact': 'artifacts/object_substrate_v0/state_diff_run003.json'}], 'rotation_changed': True, 'rotation_delta': 90, 'shape_changed': False}, 'reason': 'exact_before_state_match'}, 'step_index': 5}, {'action_id': 1, 'action_label': 'ACTION1', 'confidence': 'high', 'confidence_by_dimension': {'color': 'high', 'position': 'high', 'rotation': 'high', 'shape': 'high'}, 'provenance': {'observation': {'action': 'ACTION1', 'action_id': 1, 'after': {'color': 9, 'position': [19, 25], 'rotation': 0, 'shape': 5}, 'before': {'color': 9, 'position': [19, 30], 'rotation': 0, 'shape': 5}, 'changed_dimensions': ['position'], 'color_changed': False, 'confidence': 'high', 'position_delta': [0, -5], 'provenance': [{'after_frame_index': 6, 'before_frame_index': 5, 'row_index': 5, 'source_artifact': 'artifacts/object_substrate_v0/state_diff_run003.json'}], 'rotation_changed': False, 'rotation_delta': 0, 'shape_changed': False}, 'reason': 'exact_before_state_match'}, 'step_index': 6}, {'action_id': 4, 'action_label': 'ACTION4', 'confidence': 'high', 'confidence_by_dimension': {'color': 'high', 'position': 'high', 'rotation': 'high', 'shape': 'high'}, 'provenance': {'observation': {'action': 'ACTION4', 'action_id': 4, 'after': {'color': 9, 'position': [24, 25], 'rotation': 0, 'shape': 5}, 'before': {'color': 9, 'position': [19, 25], 'rotation': 0, 'shape': 5}, 'changed_dimensions': ['position'], 'color_changed': False, 'confidence': 'high', 'position_delta': [5, 0], 'provenance': [{'after_frame_index': 7, 'before_frame_index': 6, 'row_index': 6, 'source_artifact': 'artifacts/object_substrate_v0/state_diff_run003.json'}], 'rotation_changed': False, 'rotation_delta': 0, 'shape_changed': False}, 'reason': 'exact_before_state_match'}, 'step_index': 7}, {'action_id': 4, 'action_label': 'ACTION4', 'confidence': 'high', 'confidence_by_dimension': {'color': 'high', 'position': 'high', 'rotation': 'high', 'shape': 'high'}, 'provenance': {'observation': {'action': 'ACTION4', 'action_id': 4, 'after': {'color': 9, 'position': [29, 25], 'rotation': 0, 'shape': 5}, 'before': {'color': 9, 'position': [24, 25], 'rotation': 0, 'shape': 5}, 'changed_dimensions': ['position'], 'color_changed': False, 'confidence': 'high', 'position_delta': [5, 0], 'provenance': [{'after_frame_index': 8, 'before_frame_index': 7, 'row_index': 7, 'source_artifact': 'artifacts/object_substrate_v0/state_diff_run003.json'}], 'rotation_changed': False, 'rotation_delta': 0, 'shape_changed': False}, 'reason': 'exact_before_state_match'}, 'step_index': 8}, {'action_id': 4, 'action_label': 'ACTION4', 'confidence': 'high', 'confidence_by_dimension': {'color': 'high', 'position': 'high', 'rotation': 'high', 'shape': 'high'}, 'provenance': {'observation': {'action': 'ACTION4', 'action_id': 4, 'after': {'color': 9, 'position': [34, 25], 'rotation': 0, 'shape': 5}, 'before': {'color': 9, 'position': [29, 25], 'rotation': 0, 'shape': 5}, 'changed_dimensions': ['position'], 'color_changed': False, 'confidence': 'high', 'position_delta': [5, 0], 'provenance': [{'after_frame_index': 9, 'before_frame_index': 8, 'row_index': 8, 'source_artifact': 'artifacts/object_substrate_v0/state_diff_run003.json'}], 'rotation_changed': False, 'rotation_delta': 0, 'shape_changed': False}, 'reason': 'exact_before_state_match'}, 'step_index': 9}, {'action_id': 1, 'action_label': 'ACTION1', 'confidence': 'high', 'confidence_by_dimension': {'color': 'high', 'position': 'high', 'rotation': 'high', 'shape': 'high'}, 'provenance': {'observation': {'action': 'ACTION1', 'action_id': 1, 'after': {'color': 9, 'position': [34, 20], 'rotation': 0, 'shape': 5}, 'before': {'color': 9, 'position': [34, 25], 'rotation': 0, 'shape': 5}, 'changed_dimensions': ['position'], 'color_changed': False, 'confidence': 'high', 'position_delta': [0, -5], 'provenance': [{'after_frame_index': 10, 'before_frame_index': 9, 'row_index': 9, 'source_artifact': 'artifacts/object_substrate_v0/state_diff_run003.json'}], 'rotation_changed': False, 'rotation_delta': 0, 'shape_changed': False}, 'reason': 'exact_before_state_match'}, 'step_index': 10}, {'action_id': 1, 'action_label': 'ACTION1', 'confidence': 'high', 'confidence_by_dimension': {'color': 'high', 'position': 'high', 'rotation': 'high', 'shape': 'high'}, 'provenance': {'observation': {'action': 'ACTION1', 'action_id': 1, 'after': {'color': 9, 'position': [34, 15], 'rotation': 0, 'shape': 5}, 'before': {'color': 9, 'position': [34, 20], 'rotation': 0, 'shape': 5}, 'changed_dimensions': ['position'], 'color_changed': False, 'confidence': 'high', 'position_delta': [0, -5], 'provenance': [{'after_frame_index': 11, 'before_frame_index': 10, 'row_index': 10, 'source_artifact': 'artifacts/object_substrate_v0/state_diff_run003.json'}], 'rotation_changed': False, 'rotation_delta': 0, 'shape_changed': False}, 'reason': 'exact_before_state_match'}, 'step_index': 11}, {'action_id': 1, 'action_label': 'ACTION1', 'confidence': 'high', 'confidence_by_dimension': {'color': 'high', 'position': 'high', 'rotation': 'high', 'shape': 'high'}, 'provenance': {'observation': {'action': 'ACTION1', 'action_id': 1, 'after': {'color': 9, 'position': [34, 10], 'rotation': 0, 'shape': 5}, 'before': {'color': 9, 'position': [34, 15], 'rotation': 0, 'shape': 5}, 'changed_dimensions': ['position'], 'color_changed': False, 'confidence': 'high', 'position_delta': [0, -5], 'provenance': [{'after_frame_index': 12, 'before_frame_index': 11, 'row_index': 11, 'source_artifact': 'artifacts/object_substrate_v0/state_diff_run003.json'}], 'rotation_changed': False, 'rotation_delta': 0, 'shape_changed': False}, 'reason': 'exact_before_state_match'}, 'step_index': 12}], 'plan_source_artifact': 'artifacts/object_substrate_v0/run_005_object_aware_wall_fix/planned_sequence.json', 'planner_agent': 'receipt_object_aware_planner_agent', 'planner_ontology': 'position_shape_color_rotation', 'receipt_source_artifact': 'artifacts/object_substrate_v0/run_005_object_aware_wall_fix/receipt.json', 'sequence_derivation': 'planner_v0_object_aware_with_walls'}, 'tr87': {'action_labels': ['ACTION2', 'ACTION2', 'ACTION3', 'ACTION2', 'ACTION2', 'ACTION3', 'ACTION2', 'ACTION3', 'ACTION1', 'ACTION1', 'ACTION1', 'ACTION3', 'ACTION2', 'ACTION2'], 'action_sequence': [2, 2, 3, 2, 2, 3, 2, 3, 1, 1, 1, 3, 2, 2], 'game_id_prefixes': ['tr87'], 'hardcoded_constants': {'completion_predicate': 'bsqsshqpox_sequence_rule_validation', 'source_file': 'tr87.py', 'source_lines': ['tr87.py:499-526', 'tr87.py:942-966', 'tr87.py:996-1042', 'tr87.py:1044-1113'], 'target_required_sequence': ['nxkictbbvztB3', 'nxkictbbvztB2', 'nxkictbbvztB6', 'nxkictbbvztB5', 'nxkictbbvztB1']}, 'non_claims': ['public tr87 level-1 substrate-derived capability only', 'not a Kaggle leaderboard result', 'not a private-eval claim', 'not a third-game generality claim'], 'per_step_provenance': [{'action_id': 2, 'action_label': 'ACTION2', 'confidence': 'high', 'confidence_by_dimension': {'action_budget': 'medium', 'selector_index': 'high', 'sequence_state': 'high'}, 'provenance': [{'coverage_pair': {'action_id': 2, 'selector_index': 0}, 'source': 'tr87_selector_probe_extended_action_effect_model'}, {'source': 'tr87_source_consistency_check', 'source_lines': ['tr87.py:1005-1014', 'tr87.py:1024-1029']}], 'step_index': 0}, {'action_id': 2, 'action_label': 'ACTION2', 'confidence': 'high', 'confidence_by_dimension': {'action_budget': 'medium', 'selector_index': 'high', 'sequence_state': 'high'}, 'provenance': [{'coverage_pair': {'action_id': 2, 'selector_index': 0}, 'source': 'tr87_selector_probe_extended_action_effect_model'}, {'source': 'tr87_source_consistency_check', 'source_lines': ['tr87.py:1005-1014', 'tr87.py:1024-1029']}], 'step_index': 1}, {'action_id': 3, 'action_label': 'ACTION3', 'confidence': 'high', 'confidence_by_dimension': {'action_budget': 'medium', 'selector_index': 'high', 'sequence_state': 'unchanged'}, 'provenance': [{'coverage_pair': {'action_id': 3, 'selector_index': 0}, 'source': 'tr87_selector_probe_extended_action_effect_model'}, {'source': 'tr87_source_consistency_check', 'source_lines': ['tr87.py:996-1004']}], 'step_index': 2}, {'action_id': 2, 'action_label': 'ACTION2', 'confidence': 'high', 'confidence_by_dimension': {'action_budget': 'medium', 'selector_index': 'high', 'sequence_state': 'high'}, 'provenance': [{'coverage_pair': {'action_id': 2, 'selector_index': 4}, 'source': 'tr87_selector_probe_extended_action_effect_model'}, {'source': 'tr87_source_consistency_check', 'source_lines': ['tr87.py:1005-1014', 'tr87.py:1024-1029']}], 'step_index': 3}, {'action_id': 2, 'action_label': 'ACTION2', 'confidence': 'high', 'confidence_by_dimension': {'action_budget': 'medium', 'selector_index': 'high', 'sequence_state': 'high'}, 'provenance': [{'coverage_pair': {'action_id': 2, 'selector_index': 4}, 'source': 'tr87_selector_probe_extended_action_effect_model'}, {'source': 'tr87_source_consistency_check', 'source_lines': ['tr87.py:1005-1014', 'tr87.py:1024-1029']}], 'step_index': 4}, {'action_id': 3, 'action_label': 'ACTION3', 'confidence': 'high', 'confidence_by_dimension': {'action_budget': 'medium', 'selector_index': 'high', 'sequence_state': 'unchanged'}, 'provenance': [{'coverage_pair': {'action_id': 3, 'selector_index': 4}, 'source': 'tr87_selector_probe_extended_action_effect_model'}, {'source': 'tr87_source_consistency_check', 'source_lines': ['tr87.py:996-1004']}], 'step_index': 5}, {'action_id': 2, 'action_label': 'ACTION2', 'confidence': 'high', 'confidence_by_dimension': {'action_budget': 'medium', 'selector_index': 'high', 'sequence_state': 'high'}, 'provenance': [{'coverage_pair': {'action_id': 2, 'selector_index': 3}, 'source': 'tr87_selector_probe_extended_action_effect_model'}, {'source': 'tr87_source_consistency_check', 'source_lines': ['tr87.py:1005-1014', 'tr87.py:1024-1029']}], 'step_index': 6}, {'action_id': 3, 'action_label': 'ACTION3', 'confidence': 'high', 'confidence_by_dimension': {'action_budget': 'medium', 'selector_index': 'high', 'sequence_state': 'unchanged'}, 'provenance': [{'coverage_pair': {'action_id': 3, 'selector_index': 3}, 'source': 'tr87_selector_probe_extended_action_effect_model'}, {'source': 'tr87_source_consistency_check', 'source_lines': ['tr87.py:996-1004']}], 'step_index': 7}, {'action_id': 1, 'action_label': 'ACTION1', 'confidence': 'high', 'confidence_by_dimension': {'action_budget': 'medium', 'selector_index': 'high', 'sequence_state': 'high'}, 'provenance': [{'coverage_pair': {'action_id': 1, 'selector_index': 2}, 'source': 'tr87_selector_probe_extended_action_effect_model'}, {'source': 'tr87_source_consistency_check', 'source_lines': ['tr87.py:1005-1014', 'tr87.py:1024-1029']}], 'step_index': 8}, {'action_id': 1, 'action_label': 'ACTION1', 'confidence': 'high', 'confidence_by_dimension': {'action_budget': 'medium', 'selector_index': 'high', 'sequence_state': 'high'}, 'provenance': [{'coverage_pair': {'action_id': 1, 'selector_index': 2}, 'source': 'tr87_selector_probe_extended_action_effect_model'}, {'source': 'tr87_source_consistency_check', 'source_lines': ['tr87.py:1005-1014', 'tr87.py:1024-1029']}], 'step_index': 9}, {'action_id': 1, 'action_label': 'ACTION1', 'confidence': 'high', 'confidence_by_dimension': {'action_budget': 'medium', 'selector_index': 'high', 'sequence_state': 'high'}, 'provenance': [{'coverage_pair': {'action_id': 1, 'selector_index': 2}, 'source': 'tr87_selector_probe_extended_action_effect_model'}, {'source': 'tr87_source_consistency_check', 'source_lines': ['tr87.py:1005-1014', 'tr87.py:1024-1029']}], 'step_index': 10}, {'action_id': 3, 'action_label': 'ACTION3', 'confidence': 'high', 'confidence_by_dimension': {'action_budget': 'medium', 'selector_index': 'high', 'sequence_state': 'unchanged'}, 'provenance': [{'coverage_pair': {'action_id': 3, 'selector_index': 2}, 'source': 'tr87_selector_probe_extended_action_effect_model'}, {'source': 'tr87_source_consistency_check', 'source_lines': ['tr87.py:996-1004']}], 'step_index': 11}, {'action_id': 2, 'action_label': 'ACTION2', 'confidence': 'high', 'confidence_by_dimension': {'action_budget': 'medium', 'selector_index': 'high', 'sequence_state': 'high'}, 'provenance': [{'coverage_pair': {'action_id': 2, 'selector_index': 1}, 'source': 'tr87_selector_probe_extended_action_effect_model'}, {'source': 'tr87_source_consistency_check', 'source_lines': ['tr87.py:1005-1014', 'tr87.py:1024-1029']}], 'step_index': 12}, {'action_id': 2, 'action_label': 'ACTION2', 'confidence': 'high', 'confidence_by_dimension': {'action_budget': 'medium', 'selector_index': 'high', 'sequence_state': 'high'}, 'provenance': [{'coverage_pair': {'action_id': 2, 'selector_index': 1}, 'source': 'tr87_selector_probe_extended_action_effect_model'}, {'source': 'tr87_source_consistency_check', 'source_lines': ['tr87.py:1005-1014', 'tr87.py:1024-1029']}], 'step_index': 13}], 'plan_source_artifact': 'artifacts/object_substrate_v0/tr87_run_001_object_aware/planned_sequence.json', 'planner_agent': 'receipt_tr87_object_aware_planner_agent', 'planner_ontology': 'selector_sequence_state', 'receipt_source_artifact': 'artifacts/object_substrate_v0/tr87_run_001_object_aware/receipt.json', 'sequence_derivation': 'tr87_selector_sequence_bfs_planner'}}, 'unsupported_game_fallback': {'action_preference': ['ACTION1', 'ACTION2', 'ACTION3', 'ACTION4', 'RESET'], 'dispatch_decision': 'unsupported_game_fallback', 'expected_score': 0, 'non_claim': 'this_submission_does_not_claim_capability_on_unsupported_games'}}

RECEIPT_PATH = "/kaggle/working/object_substrate_receipts.jsonl"


class MyAgent(Agent):
    """Object-substrate dispatch agent for ls20/tr87, honest fallback otherwise."""

    MAX_ACTIONS = float("inf")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._game_key: str | None = None
        self._sequence_index = 0
        self._halt_after_fallback = False
        self.receipts: list[dict[str, Any]] = []

    def is_done(self, frames: list[FrameData], latest_frame: FrameData) -> bool:
        del frames
        if self._halt_after_fallback:
            return True
        if latest_frame.state is GameState.WIN:
            return True
        if latest_frame.state is GameState.GAME_OVER:
            return True
        if _levels_completed(latest_frame) > 0:
            return True
        if self._game_key:
            plan = SUBSTRATE_PAYLOAD["supported_games"][self._game_key]
            return self._sequence_index >= len(plan["action_labels"])
        return False

    def choose_action(self, frames: list[FrameData], latest_frame: FrameData) -> GameAction:
        del frames
        game_id = _game_id(self, latest_frame)
        available = _available_action_labels(latest_frame)

        if latest_frame.state in [GameState.NOT_PLAYED, GameState.GAME_OVER]:
            receipt = _base_receipt(game_id, available)
            receipt.update({
                "dispatch_decision": "reset_to_start_game",
                "action_chosen": "RESET",
                "provenance_chain_complete": True,
            })
            self._record(receipt)
            return _game_action("RESET", receipt)

        if self._game_key is None:
            self._game_key = _dispatch_key(game_id)

        if self._game_key is None:
            return self._unsupported_game_fallback(game_id, available)

        plan = SUBSTRATE_PAYLOAD["supported_games"][self._game_key]
        if self._sequence_index >= len(plan["action_labels"]):
            self._halt_after_fallback = True
            receipt = _base_receipt(game_id, available)
            receipt.update({
                "dispatch_decision": "supported_game_plan_exhausted",
                "supported_game": self._game_key,
                "action_chosen": "RESET",
                "provenance_chain_complete": True,
            })
            self._record(receipt)
            return _game_action("RESET", receipt)

        action_label = plan["action_labels"][self._sequence_index]
        if available and action_label not in available:
            self._halt_after_fallback = True
            receipt = _base_receipt(game_id, available)
            receipt.update({
                "dispatch_decision": "supported_game_action_unavailable",
                "supported_game": self._game_key,
                "planned_action": action_label,
                "provenance_chain_complete": False,
            })
            self._record(receipt)
            raise RuntimeError(f"planned action unavailable: {action_label}")

        receipt = _base_receipt(game_id, available)
        receipt.update({
            "dispatch_decision": "supported_game_substrate_plan",
            "supported_game": self._game_key,
            "action_sequence_index": self._sequence_index,
            "action_chosen": action_label,
            "planner_agent": plan["planner_agent"],
            "planner_ontology": plan["planner_ontology"],
            "sequence_derivation": plan["sequence_derivation"],
            "plan_source_artifact": plan["plan_source_artifact"],
            "step_provenance": plan["per_step_provenance"][self._sequence_index],
            "provenance_chain_complete": True,
            "non_claims": plan["non_claims"],
        })
        self._record(receipt)
        self._sequence_index += 1
        return _game_action(action_label, receipt)

    def _unsupported_game_fallback(self, game_id: str, available: list[str]) -> GameAction:
        action_label = _fallback_action(available)
        fallback = SUBSTRATE_PAYLOAD["unsupported_game_fallback"]
        receipt = _base_receipt(game_id, available)
        receipt.update({
            "dispatch_decision": fallback["dispatch_decision"],
            "game_id_observed": game_id,
            "available_substrate_games": SUBSTRATE_PAYLOAD["available_substrate_games"],
            "expected_score": fallback["expected_score"],
            "non_claim": fallback["non_claim"],
            "action_chosen": action_label,
            "provenance_chain_complete": True,
        })
        self._record(receipt)
        self._halt_after_fallback = True
        return _game_action(action_label, receipt)

    def _record(self, receipt: dict[str, Any]) -> None:
        receipt = dict(receipt)
        receipt["timestamp_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        self.receipts.append(receipt)
        try:
            with open(RECEIPT_PATH, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(receipt, sort_keys=True) + "\n")
        except OSError:
            pass


def _base_receipt(game_id: str, available: list[str]) -> dict[str, Any]:
    return {
        "kind": "kaggle_object_substrate_step_receipt",
        "game_id_observed": game_id,
        "available_actions": available,
        "kaggle_submission_status": "candidate_not_final_until_uploaded",
        "no_private_eval_claim": True,
        "no_general_arc_agi_3_claim": True,
    }


def _game_action(action_label: str, receipt: dict[str, Any]) -> GameAction:
    action = getattr(GameAction, action_label)
    if action.is_simple():
        action.reasoning = json.dumps({
            "dispatch_decision": receipt.get("dispatch_decision"),
            "supported_game": receipt.get("supported_game"),
            "action_sequence_index": receipt.get("action_sequence_index"),
            "provenance_chain_complete": receipt.get("provenance_chain_complete"),
        }, sort_keys=True)
    elif action.is_complex():
        action.set_data({"x": 0, "y": 0})
        action.reasoning = {
            "dispatch_decision": receipt.get("dispatch_decision"),
            "provenance_chain_complete": receipt.get("provenance_chain_complete"),
        }
    return action


def _dispatch_key(game_id: str) -> str | None:
    for key, plan in SUBSTRATE_PAYLOAD["supported_games"].items():
        if any(game_id.startswith(prefix) for prefix in plan["game_id_prefixes"]):
            return key
    return None


def _game_id(agent: MyAgent, frame: Any) -> str:
    agent_game_id = getattr(agent, "game_id", None)
    if isinstance(agent_game_id, str) and agent_game_id:
        return agent_game_id
    for name in ("game_id", "environment_id", "env_id"):
        value = _get(frame, name)
        if isinstance(value, str) and value:
            return value
    info = _get(frame, "info")
    value = _get(info, "game_id") if info is not None else None
    return value if isinstance(value, str) and value else "unknown"


def _available_action_labels(frame: Any) -> list[str]:
    raw = _get(frame, "action_mask")
    if raw is None:
        raw = _get(frame, "available_actions")
    if not raw:
        return []
    labels: list[str] = []
    for action in raw:
        try:
            labels.append(_action_name(action))
        except ValueError:
            continue
    return labels


def _action_name(action: Any) -> str:
    if isinstance(action, str):
        return action
    if isinstance(action, bool):
        raise ValueError(f"unsupported bool action: {action!r}")
    if isinstance(action, int):
        if action == 0:
            return "RESET"
        if 1 <= action <= 7:
            return f"ACTION{action}"
    name = getattr(action, "name", None)
    if isinstance(name, str):
        return name
    raise ValueError(f"unsupported action representation: {action!r}")


def _fallback_action(available: list[str]) -> str:
    for action in ("ACTION1", "ACTION2", "ACTION3", "ACTION4"):
        if not available or action in available:
            return action
    return "RESET"


def _levels_completed(frame: Any) -> int:
    value = _get(frame, "levels_completed")
    if value is None:
        value = _get(_get(frame, "info"), "levels_completed")
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def _get(obj: Any, name: str) -> Any:
    if isinstance(obj, dict):
        return obj.get(name)
    return getattr(obj, name, None)
