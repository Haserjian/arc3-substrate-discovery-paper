# ARC-AGI-3 Object-Substrate Submission Candidate

Status: historical pre-submission package snapshot.

This directory is a packaging variant captured before submission. It is not the
artifact that was submitted to Kaggle. The submitted entry is the notebook under
`kaggle/notebook_candidate/`, which was uploaded and succeeded with Kaggle public
score `0.0` (see `kaggle/submission_record/submission_record.json`).

This package candidate contains a package-local dispatch entrypoint:
`submission_entrypoint.py` exposes `SubmissionAgent.is_done(...)` and
`SubmissionAgent.choose_action(...)`.

Supported public-game substrates:

- `ls20`: run_005 object-aware planner-derived sequence.
- `tr87`: run_001 selector/sequence planner-derived sequence.

Unsupported games use one safe fallback action and then halt with an in-memory
receipt that states unsupported-game non-claims. Public scorecards are not
Kaggle leaderboard evidence.
