"""Package-local object-substrate submission candidate.

This entrypoint is self-contained for packaging preflight. It dispatches to
planner-derived public-game action sequences for ls20 and tr87, and fails fast
with a receipt-backed fallback on unsupported games. It is not a Kaggle
submission until a separate external submit gate is authorized.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ACTION_NAMES = ("RESET", "ACTION1", "ACTION2", "ACTION3", "ACTION4", "ACTION5", "ACTION6", "ACTION7")


def _load_payload() -> dict[str, Any]:
    with (Path(__file__).resolve().parent / "substrate_plans.json").open() as fh:
        return json.load(fh)


SUBSTRATE_PAYLOAD = _load_payload()


class SubmissionAgent:
    """Kaggle-contract candidate with is_done/choose_action methods."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        del args, kwargs
        self._game_key: str | None = None
        self._sequence_index = 0
        self._halt_after_fallback = False
        self.receipts: list[dict[str, Any]] = []

    def is_done(self, frames: list[Any], latest_frame: Any) -> bool:
        del frames
        if self._halt_after_fallback:
            return True
        if _terminal(latest_frame):
            return True
        if _levels_completed(latest_frame) > 0:
            return True
        if self._game_key:
            plan = SUBSTRATE_PAYLOAD["supported_games"][self._game_key]
            return self._sequence_index >= len(plan["action_labels"])
        return False

    def choose_action(self, frames: list[Any], latest_frame: Any) -> dict[str, Any]:
        del frames
        game_id = _game_id(latest_frame)
        available = _available_action_labels(latest_frame)
        if self._game_key is None:
            self._game_key = _dispatch_key(game_id)
        if self._game_key is None:
            return self._unsupported_game_fallback(game_id, available)

        plan = SUBSTRATE_PAYLOAD["supported_games"][self._game_key]
        if self._sequence_index >= len(plan["action_labels"]):
            self._halt_after_fallback = True
            return {"name": "RESET"}
        action_label = plan["action_labels"][self._sequence_index]
        if available and action_label not in available:
            self._halt_after_fallback = True
            receipt = _base_receipt(game_id, available)
            receipt.update(
                {
                    "dispatch_decision": "supported_game_action_unavailable",
                    "supported_game": self._game_key,
                    "planned_action": action_label,
                    "provenance_chain_complete": False,
                }
            )
            self.receipts.append(receipt)
            raise RuntimeError(f"planned action unavailable: {action_label}")

        receipt = _base_receipt(game_id, available)
        receipt.update(
            {
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
            }
        )
        self.receipts.append(receipt)
        self._sequence_index += 1
        return {"name": action_label}

    def _unsupported_game_fallback(self, game_id: str, available: list[str]) -> dict[str, Any]:
        action = _fallback_action(available)
        receipt = _base_receipt(game_id, available)
        fallback = SUBSTRATE_PAYLOAD["unsupported_game_fallback"]
        receipt.update(
            {
                "dispatch_decision": fallback["dispatch_decision"],
                "game_id_observed": game_id,
                "available_substrate_games": SUBSTRATE_PAYLOAD["available_substrate_games"],
                "expected_score": fallback["expected_score"],
                "non_claim": fallback["non_claim"],
                "action_chosen": action,
                "provenance_chain_complete": True,
            }
        )
        self.receipts.append(receipt)
        self._halt_after_fallback = True
        return {"name": action}


def _base_receipt(game_id: str, available: list[str]) -> dict[str, Any]:
    return {
        "kind": "kaggle_submission_candidate_step_receipt",
        "game_id_observed": game_id,
        "available_actions": available,
        "kaggle_submission_status": "not_submitted",
        "no_private_eval_claim": True,
        "no_general_arc_agi_3_claim": True,
    }


def _dispatch_key(game_id: str) -> str | None:
    for key, plan in SUBSTRATE_PAYLOAD["supported_games"].items():
        if any(game_id.startswith(prefix) for prefix in plan["game_id_prefixes"]):
            return key
    return None


def _game_id(frame: Any) -> str:
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
    labels = []
    for action in raw:
        labels.append(_action_name(action))
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


def _terminal(frame: Any) -> bool:
    flags = _get(frame, "terminal_flags")
    if isinstance(flags, dict):
        return bool(flags.get("terminal") or flags.get("win") or flags.get("game_over"))
    state = _get(frame, "state")
    state_name = _get(state, "name") if state is not None else None
    return state_name in {"WIN", "GAME_OVER"}


def _levels_completed(frame: Any) -> int:
    value = _get(frame, "levels_completed")
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def _get(obj: Any, name: str) -> Any:
    if isinstance(obj, dict):
        return obj.get(name)
    return getattr(obj, name, None)
