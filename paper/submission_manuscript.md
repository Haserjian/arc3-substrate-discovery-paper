# Failure-Driven Substrate Discovery for ARC-AGI-3

Subtitle:

A receipt-governed human-in-the-loop development study across public game
ontologies


## Abstract

We report a linked Kaggle submission with Kaggle public score `0.0`, alongside
public-scorecard level-1 completions on two structurally distinct ARC-AGI-3
games: `ls20` and `tr87`. This separation is intentional. The submitted
package is scoped to two identified public-game substrates and should not be
expected to score on unseen ontologies. The paper's contribution is therefore
not a general ARC-AGI-3 agent, but a receipt-governed human-in-the-loop
development discipline for identifying the substrate a game requires when its
state, action, and target ontology are unknown.

This is a human-accelerated development study, not a claim of autonomous
substrate discovery. Diagnostic traces exposed substrate gaps; in some cases,
source inspection was used inside a disclosed research boundary to validate or
instantiate missing mechanics. The contribution is the receipt discipline that
prevents such source-informed artifacts from being promoted into unsupported
claims of autonomous ontology discovery, general ARC-AGI-3 capability, or
private-eval performance.

The development discipline turns failed interactive runs into auditable substrate gaps. It
records diagnostic traces, separates observed/refuted/unknown claims, builds
the smallest ontology supported by evidence, locally verifies candidate plans,
and performs at most one official execution per gated attempt. On `ls20`, this
process produced a substrate-derived level-1 completion with public-scorecard score
`3.57`, `1` level completed, and `13` actions (App. A, C22).
On `tr87`, after building a separate selector/sequence ontology and closing
action-effect coverage with a targeted probe, it produced a level-1 completion
with public-scorecard score `4.76`, `1` level completed, `14` actions, zero
prediction mismatches, and complete provenance (App. A, C36, C37).

The central finding is that the development discipline transferred while the
game ontology did not.
It produced official level-1 capability on `ls20` and `tr87`, then
characterized a third ontology in `cn04`: click-selected sprite manipulation
with movement, rotation/cycling, masking, and marker-completion (App. A, C27, C38, C39).
The linked Kaggle score `0.0` is consistent with that thesis: a deliberately
ontology-specific package is not evidence of private-eval generality. The
public scorecards show what the development discipline produced when the
substrate was identified and instantiated; the Kaggle ledger records the
current competition score honestly
(App. A, C01, C17, C40).

## Claim Boundary

This paper claims that a receipt-backed, human-in-the-loop failure-analysis
loop can convert ARC-AGI-3 diagnostic failures into bounded substrate knowledge
and scoped public-game capability. It demonstrates this with level-1 public
scorecard completions on `ls20` and `tr87`, and an audit-only ontology
characterization on `cn04`. **Explicit non-claims:** this work does not claim a
general ARC-AGI-3 agent, autonomous substrate discovery, positive Kaggle
leaderboard capability, private-eval capability, or all-level performance on
any game.

## Introduction

ARC-AGI-3 agents can fail before planning begins. A system can explore broadly
and still use the wrong kind of world model: a motion heuristic on a selector
game, an actor extractor on a click-selected sprite composition task, or a
target-matching goal detector where completion is sequence validation. This
paper studies that failure mode: substrate-identification failure.

ARC-AGI-3 is interactive. Agents must explore novel environments, infer goals,
build models, and execute action-efficient plans without explicit
natural-language instructions [@ARCAGI3Track; @ARCAGI3Benchmark2026].
Official scoring is based on completion and action efficiency, not on internal
reasoning volume [@ARCAGI3Methodology]. Planning is therefore downstream of a
more basic question: what state, actions, and goals are available to be planned
over?

A substrate is the set of game-specific facts a planner needs before planning
has a coherent target: what counts as actor state, which action effects are
stable, what a goal looks like, which frame conventions can be trusted, and
when an observed mismatch is a repairable format issue rather than a
game-mechanic gap. The method begins with diagnostic runs and treats every
mismatch as a claim-bound event. Evidence is triaged into observed, refuted,
and unknown claims. A capability run is
allowed only after perception, action effects, target semantics, and local
verification are specific enough to justify one official attempt.

This is not a high-score leaderboard paper or an autonomous-discovery paper.
The Paper Prize requires a linked
Kaggle code submission and uses that linked score for the Accuracy category
[@ARCPrize2026Paper]. Our linked Kaggle submission succeeded with Kaggle public score `0.0` (App. A, C01).
That score is not hidden or reinterpreted; it marks the current generalization
boundary of a deliberately scoped substrate package. The paper separately
contributes an auditable human-in-the-loop development method, two scoped public scorecard
completions, and one additional third-game ontology audit: `ls20` level 1,
`tr87` level 1, and `cn04` substrate characterization (App. A, C22, C36, C39). Accuracy,
in the Kaggle ledger, is weak. Theory, Progress, Completeness, and scoped
cross-ontology applicability are where the evidence is strongest.

## Related Work

The ARC-AGI-3 benchmark paper defines the setting: interactive environments
where agents must explore, infer goals, build internal dynamics models, and
plan without natural-language instructions [@ARCAGI3Benchmark2026]. This paper
does not introduce those benchmark requirements. It studies a receipt-backed
development discipline for identifying the substrate a planner is allowed to
use.

Recent work on executable world models occupies a different and broader
capability lane. "Executable World Models for ARC-AGI-3 in the Era of Coding
Agents" reports a coding-agent system that builds executable Python world
models, verifies them against observations, refactors toward simpler
abstractions, and plans through the model. It reports substantially broader
public-game performance than this paper [@Rodionov2026EWM]. This paper is not a smaller version of that result. Executable-world-model work
demonstrates raw capability through constructed models; this paper studies the
prior question of how to identify what substrate should be modeled when the
ontology is unknown. Its empirical contribution is the boundary between what
transfers across games, the development discipline, and what does not, the
per-game ontology. Whereas executable world models show that mechanics can be
encoded and planned through once a representation is available, this paper
studies the receipt-governed process for deciding which representation is
claim-supported enough to use.

Graph-based exploration and map-then-act work similarly show that systematic
state/action coverage and pre-execution mapping are strong baselines
[@RudakovEtAl2025Graph; @LiuEtAl2026MAP]. This paper does not claim those
ideas as new. Its narrower contribution is the receipt-backed gate from sparse
coverage to targeted probes to planner attempts, and the stop rule that blocks further
official reruns when a gap becomes architectural rather than another bounded
format repair (App. A, C26).

The novelty boundary is therefore:

- failure-driven substrate discovery backed by receipts,
- an explicit claim inventory with observed/refuted/unknown tiers,
- cross-game evidence that the development discipline transferred while
  ontology did not,
- a substrate-gap taxonomy that distinguishes bounded frame-format gaps from
  larger game-mechanic gaps, and
- coverage-gated progression from sparse action effects to targeted probes to
  official planner attempts.

## Method: Failure-Driven Substrate Discovery

The method has six steps.

1. Run a bounded diagnostic or substrate attempt and preserve receipts.
2. Extract candidate state/action/target structure from frames and source where
   allowed.
3. Classify each claim as observed, refuted, or unknown.
4. Build the smallest ontology that the evidence supports.
5. Locally verify a planned action sequence before official execution.
6. Run officially once, then stop on completion, mismatch, provenance break, or
   a named substrate gap.

### Algorithm 1: Failure-Driven Substrate Discovery

| Step | Operation |
|---:|---|
| Input | game instance `g`, interaction budget `B`, and claim ledger `L` |
| Output | substrate `S`, capability receipt `R`, or named gap `G` |
| 1 | Execute a bounded diagnostic probe or substrate attempt under budget `B` |
| 2 | Emit receipt `R` containing frames, actions, score, state hashes, runner version, and provenance |
| 3 | Triage observations into `L_obs`, `L_refuted`, and `L_unknown` |
| 4 | Construct the smallest substrate `S` satisfying `L_obs` and not contradicting `L_refuted` |
| 5 | If action-effect coverage is below the pre-planner gate, execute a targeted structural probe or stop with `coverage_gap` |
| 6 | If local verification fails, stop with `verifier_gap` or `substrate_gap` |
| 7 | Authorize at most one official environment execution after the gate opens |
| 8 | On success, return a capability receipt; otherwise classify the failure as `frame_format_gap`, `perception_ontology_gap`, `game_mechanic_gap`, or `architecture_review_gap` |

The method intentionally separates score evidence from methodology evidence.
Score evidence comes from official scorecards, Kaggle submissions, and
environment actions. Local analysis, source inspection, and test execution
support the paper's Theory and Completeness claims, but they do not count as
ARC-AGI-3 actions and do not themselves create Kaggle-linked Accuracy evidence
[@ARCPrize2026Paper; @ARCAGI3Methodology].

### Source-Informed Evidence Boundary

Source-informed work is allowed only inside a disclosed research boundary. In
this project, source inspection informed substrates such as `ls20` wall
geometry, tr87 validation semantics, and the source-static `cn04` audit; it
also served as an oracle for local verification and source-consistency checks
(App. A, C23, C31, C39). It did not authorize private-eval generality,
autonomous-discovery claims, or source-derived action replay as a planner
claim. That distinction matters because `run_003` and `run_005` produced the
same `ls20` level-1 action sequence, but they carry different derivation
claims: `run_003` was source-derived, while `run_005` recorded
object-substrate planner provenance (App. A, C23).

Derivation and status ledger:

| Result / Artifact | Interaction-derived? | Source-informed? | Official status |
|---|---:|---:|---|
| Kaggle Record | N/A | submitted package includes source-informed components | official Kaggle submission |
| `ls20 run_005` | partly | yes, geometry | official capability run |
| `tr87 run_001` | partly | yes, validation | official capability run |
| `gamma2c.1` selector probe | yes | source-checked | non-capability coverage probe |
| `cn04 gamma3a` | limited | yes | no execution run |
| `ls20` level-2 review | limited | yes | no execution run |

Allowed-claim ledger:

| Result / Artifact | Kaggle linkage | Allowed paper claim |
|---|---|---|
| Kaggle Record | Kaggle public score `0.0` | linked Kaggle baseline |
| `ls20 run_005` | N/A | level-1 public-game completion |
| `tr87 run_001` | N/A | level-1 public-game completion |
| `gamma2c.1` selector probe | N/A | coverage gate verification, not score capability |
| `cn04 gamma3a` | N/A | ontology characterization only |
| `ls20` level-2 review | N/A | architecture-review gap, no rerun authorized |

**Automation boundary.** In the current implementation, diagnostic execution, receipt capture, selected
consistency checks, local verification, and official planner execution are
scripted. Substrate interpretation, source-informed mechanic identification,
and cross-ontology model repairs are human-authored development steps. The
paper therefore claims a receipt-governed human-in-the-loop development
discipline, not an autonomous online agent that independently induces each
substrate from environment interaction alone.

**Threat model.** The main risks are source-informed artifacts being mistaken for autonomous
discovery, local verification being mistaken for official score evidence,
repeated official attempts becoming informal leaderboard search, and
third-game audits being mistaken for capability claims. The mitigation is the
claim ledger: each artifact is assigned an evidence type, a derivation
boundary, an official/nonofficial status, and an allowed claim.

## System Architecture / Receipt Discipline

Every major result is backed by artifacts and tests. The claim inventory is the
main safety rail for object-substrate and cross-game evidence added after the
early diagnostic runs. Each claim lists artifacts, tests, and
non-claim siblings.

The paper lane keeps diagnostic evidence, planner-lane evidence,
object-substrate evidence, public scorecard evidence, and Kaggle linkage
evidence separate. This prevents a local or source-informed step from becoming
an unearned score claim. It also makes productive failures usable: each failed
attempt either tightens a substrate, refutes a hypothesis, or names a gap that
blocks another run.

The tr87 sequence is the cleanest example of coverage gating. Gamma2c found
only `4/20` action/state pairs and blocked planner work (App. A, C32).
Gamma2c.1 used a single targeted selector probe to reach `20/20`, then gamma2d
planned and completed level 1 (App. A, C33, C36).
This is not trial-and-error until success; it is process evidence that the
coverage gate changed the decision boundary before the official planner
attempt. It is not claimed as a controlled ablation.

## ls20 Case Study

The `ls20` substrate began as a motion/object ontology. The actor state tracked
position, shape, color, and rotation. Early diagnostic traces found motion
correlations and frame-shape anomalies but did not justify a goal detector
(App. A, C02-C09).

The first successful object-substrate capability result was `run_005`. It
completed level 1 with public-scorecard score `3.57`, one level completed, and 13
actions after local verification (App. A, C22).
The sequence matched the earlier source-derived handoff sequence, but the
claim boundary is different: `run_003` was source-derived while `run_005` was
planned by the object substrate and preserved planner-derived sequence
provenance (App. A, C23).

Later `ls20` work exposed the method's stop condition. `run_008` crossed the
level-1 transition online but still completed only one level and recorded
`official_local_online_divergence` (App. A, C24).
The subsequent source mechanic review emitted `architecture_review_required`
because the dynamic trigger-bound sprite automata failed the bounded-primitive
gate (App. A, C25).

That finding is part of the result, not a footnote. The method did not run
`run_009` from momentum. It classified the gap as larger than another
frame-format patch and pivoted to cross-game transfer.

## tr87 Case Study

Gamma2a tested whether the `ls20` substrate transferred to `tr87`. It did not.
The transfer audit classified the result as `method_transfers_ontology_doesnt`:
frame-shape handling transferred, while actor extraction, action effects,
target extraction, and game mechanics required tr87-specific redesign (App. A, C27).

Gamma2b then built a tr87-specific perception layer. It extracted well-formed
`Tr87ActorState` on `81/81` probe frames (App. A, C28). The
target structure was sequence-rule matching, not ls20-style position plus
shape/color/rotation equality (App. A, C29).

Gamma2c built a separate action-effect model. It analyzed 80 transitions and
identified selector-position and sequence-state effects, explicitly not motion
deltas (App. A, C30).
The consistency checker passed `80/80` source checks with mismatch count zero
(App. A, C31).

The planner did not run immediately. Gamma2c recorded only `4/20` action/state
pairs and `ready_for_gamma2d_planner: false` (App. A, C32). A targeted selector probe
then completed the coverage objective with `20/20` action-state pairs and
source consistency `1.0`, while scoring `0.0` because it was not a capability
attempt (App. A, C33, C34).

After that gate opened, gamma2d planned over selector/sequence state, locally
verified a 14-action plan, and completed tr87 level 1 officially with
public-scorecard score `4.76`, one level completed, and 14 actions (App. A, C35, C36).
The receipt recorded zero prediction mismatches and complete provenance
(App. A, C37).

## Cross-Game Results

The cross-game result is qualitative and scoped. The same method produced
official level-1 completions in two games, and then characterized a third game
ontology without attempting capability. The capability ledger is still two
games. The method-transfer ledger is now three ontologies.

| Game | Ontology Characterized | Substrate Status | Capability Status | Claim Boundary |
|---|---|---|---|---|
| `ls20` | motion plus shape/color/rotation target matching | object substrate with wall geometry and bundle handling | official level-1 completion, public-scorecard score `3.57` | not level 2+, not private-eval generality |
| `tr87` | selector index plus sequence-rule construction | tr87-specific perception, action effects, coverage probe, local verifier | official level-1 completion, public-scorecard score `4.76` | not all-level tr87 capability |
| `cn04` | click-selected sprite manipulation with movement, rotation/cycling, masking, and marker-completion | source-static substrate audit and transferability map | no official run, no planner, no capability claim | method-characterization evidence only |

Scores are rounded in the main body text; exact machine values are preserved in
the claim inventory and receipts.

`ls20` used actor position, shape/color/rotation, wall geometry,
frame-bundle handling, and exact target matching. `tr87` used selector index,
sequence slots, tile variant cycling, source-consistent action effects, and
sequence-rule target validation (App. A, C38). Gamma3a selected `cn04` because
its source exposes a third ontology: click selection (`ACTION6`), selected
sprite movement (`ACTION1` through `ACTION4`), rotation or overlapping-sprite
cycling (`ACTION5`), masking, and marker-completion (App. A, C39).

This is not a third-game completion or all-level generality claim. It is a
cross-ontology development-discipline claim: three structurally different public
games were characterized by the same evidence-gated pipeline, and two of those
substrates produced official level-1 completions. The shared contribution is
the discipline: diagnose, model, gate on coverage, verify locally when a
planner is attempted, run once, and stop on named gaps. The shared contribution
is not a single game ontology.

The earlier N=2 weakness therefore changes shape. Capability remains N=2, but
method characterization is N=3 (App. A, C39). This paper
treats this as stronger evidence for cross-ontology applicability of the
development discipline, not as proof of broad ARC-AGI-3 generality.

## Substrate-Gap Taxonomy

The artifact chain supports two operational gap classes (App. A, C26).

Frame-format gaps occur when the runner emits a frame or bundle convention the
extractor handles incorrectly while the underlying mechanic remains within the
current planner ontology. In the `ls20` chain, multi-frame transition bundles
and grayscale bundle shapes were bounded gaps: each could be named, repaired,
tested, and re-run without changing the planner's game-mechanic model.

Game-mechanic gaps occur when the current state/action model lacks a mechanic
needed for planning. `ls20` level 2 is the current example. The source review
found dynamic trigger-bound sprite automata and budgeted event semantics that
failed the bounded-primitive gate (App. A, C25).

Schematically, the `ls20` level-2 review emitted a stop decision with these
fields:

- `decision`: `architecture_review_required`
- `gap_class`: `game_mechanic_gap`
- `reason`: dynamic trigger-bound sprite automata exceeded the
  bounded-primitive gate
- `official_rerun_authorized`: `false`

The taxonomy is not claimed as an exhaustive law of ARC-AGI-3. Its value is
operational: it predicts what kind of next action is justified. Frame-format
gaps can often justify a small substrate repair and one verified rerun.
Game-mechanic gaps may require architecture review, local event-state
modeling, or a pivot. In this chain, the taxonomy's practical test was that it
blocked another `ls20` run when the failure was no longer a bundle-selection
problem.

## Limitations

The linked Kaggle submission succeeded and records Kaggle public score `0.0` (App. A, C01). The two positive scores are public
scorecard evidence on covered public games, not Kaggle leaderboard or
private-eval claims (App. A, C17, C40). This paper does not ask the reader to treat
public scorecards as a substitute for the Kaggle ledger; it asks the reader to
evaluate a methodology whose current Kaggle Accuracy evidence is weak and
honestly recorded.

The capability evidence is level-1 only in two games. `ls20` level 2 remains
an architecture-review gap (App. A, C25), and tr87 levels beyond level 1 are untested. The cross-ontology evidence is stronger after
gamma3a, but it is still asymmetric: method characterization spans `ls20`,
`tr87`, and `cn04`, while official completion evidence remains `ls20` and
`tr87` only (App. A, C39).

Several components are source-informed. They are valid local research
evidence, and the submitted package records its licensing and provenance
posture, but they do not support private-eval generality or a broad competition
framing. They also do not support a claim
that the agent autonomously discovered each substrate. The paper should be
judged on the scoped claim it makes: receipt-backed human-in-the-loop substrate
discovery produced official level-1 public scorecard completions in two
different ontologies and named the point where further `ls20` iteration became
architectural.

## Conclusion

This project began with diagnostic traces that scored `0.0`. It now has a
guarded evidence chain: diagnostic receipts, claim tiers, object-substrate
modules, coverage gates, local verifiers, a linked Kaggle submission with
Kaggle public score `0.0`, scoped public scorecard completions in two games, and a
third ontology audit for `cn04`.

What transferred was the development discipline: diagnostic traces, claim tiers, coverage
gates, local verification before official execution, and stop rules when a gap
became architectural. What did not transfer was the game ontology. `ls20`
needed motion, object attributes, wall geometry, and target matching. `tr87`
needed selector index, sequence state, and rule validation. `cn04` exposed
click-selected sprite manipulation, rotation/cycling, masking, and
marker-completion.

The main result is not that one ontology is sufficient for ARC-AGI-3. The main
result is that planning is downstream of substrate identification. Failure
traces can reveal which substrate is missing; local verification can decide
when a capability attempt is justified; and official runs should stop when the
next gap is no longer bounded. In the current evidence, that discipline
produced `ls20` and `tr87` level-1 completions and characterized `cn04` as a
third distinct ontology while showing that the development discipline
transferred across the studied public ontology types and the game ontology did
not.

The method does not remove the need for game-specific modeling. It makes that
need explicit, testable, and governed by stop rules.

## Data and Reproducibility Availability

The source repository for the submitted method is https://github.com/Haserjian/arc3-substrate-discovery-paper. The linked Kaggle notebook is https://www.kaggle.com/code/timhaserjian/arc3-object-substrate-submission-candidate. Internal evidence is cited by repo-relative artifact paths rather than local filesystem paths; the submission candidate contains no local home-directory absolute paths.

Key repo-relative evidence paths:

- artifacts/kaggle_submission_preflight/kaggle_submission_record/submission_record.json
- artifacts/object_substrate_v0/run_005_object_aware_wall_fix/receipt.json
- artifacts/object_substrate_v0/tr87_run_001_object_aware/receipt.json
- artifacts/object_substrate_v0/gamma3a_third_game_substrate_audit/game_selection.json
- artifacts/object_substrate_v0/gamma3a_third_game_substrate_audit/gamma3b_decision.json
- artifacts/object_substrate_v0/gamma3a_third_game_substrate_audit/transferability_map_vs_ls20_tr87.json
- docs/object_substrate_v0/gamma3a_third_game_substrate_audit.md
- docs/paper/cross_game_substrate_results.md
- docs/paper/substrate_gap_taxonomy.md
- docs/paper/claim_inventory.md
- docs/paper/results_table.md
- docs/paper/known_gaps.md
- artifacts/object_substrate_v0/gamma2a_cross_game_substrate_report/cross_game_substrate_report.json
- artifacts/object_substrate_v0/run_008_grayscale_bundle_fix/level2_source_mechanic_review/next_decision.json
- artifacts/object_substrate_v0/run_008_grayscale_bundle_fix/receipt.json
- artifacts/object_substrate_v0/tr87_action_effect_model/action_effect_model.json
- artifacts/object_substrate_v0/tr87_action_effect_model/consistency_check.json
- artifacts/object_substrate_v0/tr87_action_effect_model/known_gaps.json

## Appendix A: Claim Inventory Summary

This appendix is a reader-facing index to the internal claim inventory. It is not a separate score claim; the full inventory in the repository carries artifacts, tests, and non-claim siblings.
Reader summaries may shorten long machine identifiers for PDF legibility; exact identifiers are preserved in the repository inventory and receipts.

| Claim ID | Tier | Reader summary |
|---|---|---|
| C01 | OBSERVED | The ARC-AGI-3 Kaggle linkage submission succeeded and recorded Kaggle public score `0.0`. |
| C02 | OBSERVED | The `ls20` official-runner diagnostic trace scored `0.0`, completed `0` levels, and used `81` actions. |
| C03 | OBSERVED | The `ls20` rotating probe produced `81` novel states and `0` completed levels. |
| C04 | OBSERVED | `ls20` produced cardinal largest-region motion correlations for ACTION1/ACTION2/ACTION3/ACTION4 under medium-confidence action attribution. |
| C05 | OBSERVED | The tested fixed action prefix from reset matched `8/8` paired replay rows. |
| C06 | REFUTED | The hypothesis that tested direction pairs return to the exact before-frame state hash is refuted by `0/4` returns. |
| C07 | REFUTED | The clean position-level inverse hypothesis is refuted for the tested pair with position-level non-return evidence. |
| C08 | OBSERVED | Rows `42/43` in `ls20` show frame-shape changes `[1,64,64] -> [6,64,64]` and `[6,64,64] -> [1,64,64]`. |
| C09 | UNKNOWN | The best current hypothesis is that rows `42/43` may reflect a structural/render-phase event, but the semantic label is unknown. |
| C17 | REFUTED | Current artifacts explicitly refute positive Kaggle leaderboard capability and private-eval capability claims; the Kaggle public score is `0.0`. |
| C22 | OBSERVED | `run_005` completed `ls20` level 1 with score `3.571428571428571`, `1` level completed, and `13` actions after local verification passed. |
| C23 | OBSERVED | `run_005` planned sequence `[3,3,3,1,1,1,1,4,4,4,1,1,1]` matched the earlier source-derived `run_003` sequence, while `run_005` recorded planner-derived sequence provenance. |
| C24 | OBSERVED | `run_008` locally verified levels `[1,2]`, crossed the level-1 transition online, but the official run still completed only `1` level and recorded an official/local online-divergence marker. |
| C25 | OBSERVED | The level-2 source mechanic review emitted `architecture_review_required` because the source-visible dynamic trigger-bound sprite automata failed the bounded-primitive gate. |
| C26 | OBSERVED | The artifact chain supports a paper taxonomy separating bounded frame-format gaps from larger game-mechanic gaps that may require architecture review. |
| C27 | OBSERVED | The gamma2a cross-game substrate audit classified the finding as a method-transfers/ontology-does-not-transfer finding: frame/bundle and diagnostic layers transferred, while actor, action, target, and mechanic layers required tr87-specific redesign. |
| C28 | OBSERVED | The tr87-specific perception audit produced well-formed `Tr87ActorState` on `81/81` frames with coverage rate `1.0`. |
| C29 | OBSERVED | The tr87 target extractor characterized the goal as sequence-rule matching with completion predicate the source-specific sequence-rule validation predicate. |
| C30 | OBSERVED | The tr87 action-effect model analyzed `80` transitions and identified selector-position and sequence-state effects, with no motion-delta representation. |
| C31 | OBSERVED | The gamma2c consistency checker reported `80/80` transition checks passed with pass rate `1.0` and mismatch count `0`. |
| C32 | OBSERVED | Before the selector probe, gamma2c recorded only `4/20` observed action/state pairs, `16` known gaps, and planner readiness false. |
| C33 | OBSERVED | The targeted selector coverage probe observed `20/20` `(action, selector_index)` pairs, with source consistency pass rate `1.0` and planner readiness true. |
| C34 | OBSERVED | The selector coverage probe scored `0.0`, completed `0` levels, and took `20` actions while completing its coverage objective. |
| C35 | OBSERVED | The tr87 local verifier passed a `14`-action plan over selector/sequence state before official execution. |
| C36 | OBSERVED | The tr87 object-aware planner official run scored `4.761904761904762`, completed `1` level, took `14` actions, and used planned sequence `[2,2,3,2,2,3,2,3,1,1,1,3,2,2]`. |
| C37 | OBSERVED | The tr87 run_001 receipt reported zero prediction mismatches, no failure modes, and complete provenance. |
| C38 | OBSERVED | The object-substrate pipeline produced official level-1 completions for both `ls20` and `tr87`, despite `ls20` using position/shape/color/rotation matching and `tr87` using selector/sequence-rule matching. |
| C39 | OBSERVED | Gamma3a characterized `cn04` as a third distinct ontology, click-selected sprite manipulation with movement, rotation/cycling, masking, and marker-completion, while explicitly emitting `audit_only_sufficient` rather than authorizing a planner or official run. |
| C40 | REFUTED | The current evidence refutes broad claims that the project has a general ARC-AGI-3 agent, private-eval capability, or positive Kaggle leaderboard performance. |

## References

- [ARCPrize2026Paper] ARC Prize. "ARC Prize 2026 - Paper Prize". ARC Prize website. 2026. https://arcprize.org/competitions/2026/paper.
- [ARCAGI3Methodology] ARC Prize. "ARC-AGI-3 Scoring Methodology". ARC-AGI-3 Docs. 2026. https://docs.arcprize.org/methodology.
- [ARCAGI3Track] ARC Prize. "ARC Prize 2026 - ARC-AGI-3 Competition". ARC Prize website. 2026. https://arcprize.org/competitions/2026/arc-agi-3.
- [ARCAGI3Benchmark2026] ARC Prize Foundation. "ARC-AGI-3: A New Challenge for Frontier Agentic Intelligence". arXiv. 2026. arXiv:2603.24621. https://arxiv.org/abs/2603.24621.
- [Rodionov2026EWM] Sergey Rodionov. "Executable World Models for ARC-AGI-3 in the Era of Coding Agents". arXiv. 2026. arXiv:2605.05138. https://arxiv.org/abs/2605.05138.
- [RudakovEtAl2025Graph] Evgenii Rudakov, Jonathan Shock, and Benjamin Ultan Cowley. "Graph-Based Exploration for ARC-AGI-3 Interactive Reasoning Tasks". arXiv; AAAI 2026 Workshop on AI for Scientific Research. 2025. arXiv:2512.24156. https://arxiv.org/abs/2512.24156.
- [LiuEtAl2026MAP] Yuxin Liu, Ziang Ye, Yueqing Sun, Mingye Zhu, Jinwei Xiao, Zhuowen Han, Qi Gu, Xunliang Cai, and Lei Zhang. "MAP: A Map-then-Act Paradigm for Long-Horizon Interactive Agent Reasoning". arXiv. 2026. arXiv:2605.13037. https://arxiv.org/abs/2605.13037.
