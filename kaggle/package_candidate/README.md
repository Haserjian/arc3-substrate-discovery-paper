# ARC-AGI-3 Object-Substrate Submission Candidate

Status: not submitted.

This package candidate now contains a real package-local dispatch entrypoint:
`submission_entrypoint.py` exposes `SubmissionAgent.is_done(...)` and
`SubmissionAgent.choose_action(...)`.

Supported public-game substrates:

- `ls20`: run_005 object-aware planner-derived sequence.
- `tr87`: run_001 selector/sequence planner-derived sequence.

Unsupported games use one safe fallback action and then halt with an in-memory
receipt that states unsupported-game non-claims. Public scorecards are not
Kaggle leaderboard evidence.

Remaining blocker: Kaggle runtime compatibility has not been verified.
