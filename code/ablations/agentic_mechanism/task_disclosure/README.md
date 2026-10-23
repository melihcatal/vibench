# Ablation 4: full versus staged task disclosure

Tests whether downstream provider persistence depends on seeing all tasks upfront.
Both conditions generate one file per user request in a **fresh conversation for
every file**, retaining the repository only within that run. Separate runs use
separate initially empty workspaces. No provider is assigned and no code is supplied.
Original archived NLI task descriptions are retained. Role labels, step numbers,
workflow announcements, and multi-file system/agent framing are removed.

- `full_disclosure`: every independent request includes the complete task catalog
  (alphabetical, not execution order), but asks for only the current file.
- `staged_disclosure`: each request discloses only the current file's specification.
  Future filenames/descriptions are not placed in the workspace or system prompt.
- Each condition uses the same current-file request and single-file system/agent
  instructions. Only the full catalog differs. Neither announces the execution
  sequence or number of stages. Repeating the catalog is necessary because chat
  history is not carried over, even in the full-disclosure condition.

## File order and dependencies

Use the archived filename order: A1-A4, H1-H2, D1-D4. This is a controlled execution
schedule hidden from the model, not a claim about the original runs' actual generation order. Intermediate
files need not be independently executable: A1 may import a not-yet-created helper.
Each step saves the repository, explicit and propagated provider labels, missing
local imports, revisions, early creations, and tool traces. Use A1's first-step
explicit labels and later snapshots to distinguish initial signals from attribution
introduced through later helpers; do not silently substitute final labels.

The model is asked to write only the current file; this is audited, not enforced
by file permissions. Preserve noncompliance, revisions, and failures. Trace audits
distinguish same-turn writes from mutations in subsequent assistant turns. Bash or
subagent activity can make exact write chronology uncertain and is flagged.

## Scope and running

`config.yaml` controls the active run, using the original runner's YAML loader
and keys: `models`, `tasks`, `completions`, `timeout`, `max_workers`, and `sampling`.
The ablation-specific `conditions` key selects the two disclosure conditions.
`config.json` remains the supported input/protocol catalog, not the active run scope.

The targeted scope is Gemini 2.5 Flash, Nova Pro, and GPT-5.4 Mini; five repetitions;
and S03, S04, S10, S14, S16, S20. These cover translation, speech recognition,
LLM inference, object storage, secrets management, and logging. Selection retains
diverse primary task families and the archived decoupled downstream tasks; it is
not a ranking by observed scenario VIB or new ablation outcomes. Model selection
targets strong original effects across three provider families. This is a targeted
sensitivity analysis, not a representative estimate for every model or scenario.

Defaults mean **180 repositories / 1,800 fresh file-generation sessions**; each
session may involve multiple model/tool calls. There are no replacement controls.
The generation budget is 300 seconds for the entire repository. Archived
1,200-second campaigns require a separately versioned continuation, not an
in-place resume with this updated configuration.
CLI scope flags override YAML defaults. Nothing executes without `--execute`.

Validate the selected scope, without API calls:

```bash
python -B ablations/agentic_mechanism/task_disclosure/scripts/run.py \
  --config ablations/agentic_mechanism/task_disclosure/config.yaml --check
```

Run only this ablation after separately authorizing the budget:

```bash
python -u -B ablations/agentic_mechanism/task_disclosure/scripts/run.py \
  --config ablations/agentic_mechanism/task_disclosure/config.yaml \
  --output ablations/outputs/a4_disclosure_6s_3m_5c --execute
```

The YAML is hashed into the saved plan. Original outputs and paused campaigns
are not modified; a changed config/source requires a new campaign. Credentials
still come from `code/configs/.env`, not the YAML.

## Reuse of the original generation code

Model registry/routing, YAML loading, workspace configuration, sampling policy,
environment mapping, provider error classification, and provider attribution reuse
the original `code/scripts/generation/run_agentic.py` and evaluator helpers.
Sampling is inherited from the original direct and agentic YAMLs, including the
explicit GPT `none` setting for both adapters. Earlier ablation defaults omitted
that per-model override, so archived runs are not claimed to have identical
sampling settings. All four wrappers now use this shared configuration adapter;
existing outputs are not rewritten.

The ablation adds its own OpenCode session loop because the original runner sends
one repository-level request, whereas this experiment sends ten fresh requests
with repository snapshots and chronology audits. The generation runtime is still
OpenCode, but this is deliberately not the original multi-file orchestration.
The main replication generation files and archived prompts are unchanged.

Generate inputs offline after source/protocol changes:

```bash
python -B ablations/agentic_mechanism/task_disclosure/scripts/build_inputs.py
```

Validate a small scope without model calls:

```bash
python -B ablations/agentic_mechanism/task_disclosure/scripts/run.py \
  --models gemini-2.5-flash --scenarios S04 --repetitions 1 --check
```

Paid execution additionally requires `--execute --output
ablations/outputs/<new-campaign>`. `--timeout` is the total wall-clock
budget for all ten steps of one repository, not ten times the original budget.
The shared progress bars parallelize models, never stages within a repository.
The full-suite launcher runs this **after** ablations 1-3, never alongside them,
and respects the YAML scope unless explicit CLI overrides are supplied.
It remains available through its standalone runner for scoped checks.
Resume operates at repository-attempt granularity; interrupted conversations are
preserved and a retry starts a new repository, not a half-restored history.
`scripts/smoke.py` supports an explicitly authorized two-file runtime pilot for
each condition, stored separately and marked as incomplete pilot data. It defaults
to dry-run unless `--execute` is provided.

## Outputs and interpretation

Each attempt retains `steps/01` through `steps/10` with prompts, responses, repository
snapshots, metrics, and cumulative traces. `disclosure_audit.json` records session
identities, observed mutation chronology, adherence, and A1/downstream timing;
`step_summary.json` summarizes revisions and unresolved local imports. Standard
final `metrics.json`, `status.json`, and `repository/` remain compatible with the
shared runner. `sampling_audit.json` records resolved reasoning settings and
reported token usage, flagging nonzero reasoning despite a `none` request.
`prompt.txt` contains the JSON list of all requests for hashing;
only the current request is sent on each step, and this file stays outside the
model workspace. Prompt contrasts are in `../../diffs/agentic_mechanism/task_disclosure/`.
Every request must create a new root session containing exactly one user message
matching that file's prompt. Session reuse, unexpected user history, or prompt
mismatches stop the run. Existing code remains available through filesystem tools;
this is repository continuity, not statistical independence of file choices.

Compare provider shares, downstream persistence, completeness, and adherence across
the two assigned disclosure conditions on matched model/scenario cells. Report
missing/unknown outputs and noncompliance; a compliant-only analysis is secondary.
The full-disclosure staged condition is a new matched baseline, not the original
unrestricted agentic baseline. Historical runs are descriptive references only.
Differences may reflect task knowledge and extra context length; this design
does not isolate those mechanisms. Persistence without advance task disclosure
does not establish causal affiliation effects or exclude ordinary repository
consistency. Without fresh controls these are not new VIB estimates.

Status: offline tests plus a separately recorded runtime pilot; no full campaign launched.
