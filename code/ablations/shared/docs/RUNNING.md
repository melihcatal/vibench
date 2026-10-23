# Running the ablation campaigns

Each campaign has its own runner under its `scripts/` directory. Shared helpers
reuse the main OpenCode runner and LiteLLM model-call function rather than
duplicating them. No model calls occur unless `--execute` is explicitly
supplied.

**Run every command below from `code/`**, which is the import root — the
campaigns are imported as `ablations.<group>.<campaign>.scripts`. Campaign
outputs are written under `../outputs/ablations/`.

## Where the settings come from

Campaign sampling is not maintained as a separate copy. The shared configuration
adapter calls the main loaders and inherits sampling from the paper's own
configs:

- `code/configs/vibench/agentic/complete/opencode_full_5c.yaml`
- `code/configs/vibench/direct/complete/full_5c.yaml`

Both of those, plus the per-campaign YAML, are hashed into every run's
`plan.json` under `code_sha256`. Scope is set with the paper's YAML keys
(`models`, `tasks`, `completions`, `timeout`, `max_workers`) plus the
campaign-specific `conditions`; CLI flags override YAML. All campaign YAML
defaults use a 300 s timeout, and values above 300 s are rejected in both YAML
and the CLI.

## Validate without API calls

```sh
python -B -m unittest discover -s ablations/shared/tests -p 'test_*.py' -v
python -B ablations/initial_provider/assigned_as_code/scripts/run.py
python -B ablations/agentic_mechanism/single_shot_multifile/scripts/run.py
python -B ablations/initial_provider/by_instruction/scripts/run.py
```

The current five-repetition defaults plan 1,200 assigned-anchor runs, 600
single-shot runs, 1,200 runs for ablation 3, and 180 YAML-configured runs for ablation 4. These
are planning defaults, not authorization to execute the entire scope.
Dry runs validate inputs and print a plan fingerprint without creating
outputs, loading credentials, or starting OpenCode. Use `--scenarios`, `--models`,
`--conditions`, and `--repetitions` to narrow the plan. Lists are comma-separated.

## Progress and sequential ablations

The display follows the original study runner: a total progress bar with
elapsed time/ETA, plus one bar per model showing its current scenario,
condition, repetition, generated-file count, and errors. Bars count finished
attempts, including failures, not only successful generations. Models execute
in parallel, with one active job per model; `--workers N` caps concurrency and
`--sequential` makes models sequential as well. Detailed per-model events are
saved in `logs/<model>.jsonl`, with counters in `progress.json`.

The suite launcher runs ablations strictly **1, then 2, then 3**, waiting for
all model workers before the next stage. It validates every stage's scope
before making paid calls and stops on failures, including unresolved failures
from an earlier invocation. It never schedules ablation 1's `no_anchor` or
ablation 2's `agentic` baseline. This command only validates:

```sh
bash ablations/shared/scripts/run_sequential.sh \
  ../outputs/ablations/shared/new_suite \
  --models gemini-2.5-flash,nova-pro --scenarios S04 --repetitions 1 --workers 2
```

Add `--execute` only after reviewing the plan. `PYTHON_BIN` can select the
vibench environment's Python executable. Use an individual runner for `--limit`
pilots; the suite rejects partial-stage limits. On Ctrl-C, no further jobs are
scheduled and active calls finish or time out before cleanup and exit.

The example uses the roster/scenario intersection currently prepared in all
three ablations. Ablations 1/2 still need expansion for the six-model, 20-scenario
design; the launcher rejects unsupported selections rather than silently
dropping models. The S11 Google SDK decision remains a separate launch guard.

## Before a paid pilot

- Model-route audit (2026-09-18): the original five-model roster is not executable
  unchanged. DeepSeek's `deepseek-chat` alias no longer serves V3.2;
  xAI's Grok 4.1 slug redirects to Grok 4.3. Execution blocks both
  labels. See [DeepSeek's changelog](https://api-docs.deepseek.com/updates/) and
  [xAI's retirement notice](https://docs.x.ai/developers/migration/may-15-retirement).
  Mistral's `mistral-large-latest` route also needs pinning/identity verification.
  The commands below describe the proposed design, not an approved current roster.
- Configure the existing credentials in `code/configs/.env`. These are loaded only
  for execution. Canonical Nova routes now use the first-party Nova API, not a
  local Bedrock proxy. Preserve that gateway difference from original agentic
  results. The "Nova routing" note in the repository README records which
  route each run used.
- Use the original OpenCode version when available. Versions of OpenCode, Python,
  and key SDKs are recorded and checked on resume. Aliased hosted model backends
  can still change; this does not freeze remote weights.
- OpenCode tool traces are exported from its local SQLite database. The default
  is `$XDG_DATA_HOME/opencode/opencode.db`, or
  `~/.local/share/opencode/opencode.db`; override with `--trace-db` if needed.
  The runner checks the schema and does not migrate or modify the database.
- S11's Google anchor remains blocked pending a reviewed legacy SDK decision.
  Record that decision with `--s11-legacy-ack "..."` to include it. This flag
  records acknowledgement, not proof of SDK compatibility. A pilot on S04 avoids
  this unresolved issue.
- Generation does not install the anchor's dependency inventory or invoke its
  cloud services automatically. OpenCode retains its original tool permissions,
  including shell and web access. A temporary directory is not an OS sandbox:
  use a dedicated experiment account/container for host-level isolation.

## Paid pilot command examples

One S04 repetition across the two currently prepared affiliated models gives
four anchored runs for ablation 1 and two single-shot runs for ablation 2:

```sh
python -B ablations/initial_provider/assigned_as_code/scripts/run.py --models gemini-2.5-flash,nova-pro --conditions anchor_google,anchor_aws --scenarios S04 --repetitions 1 --output ../outputs/ablations/initial_provider/assigned_as_code/a1_pilot --execute
python -B ablations/agentic_mechanism/single_shot_multifile/scripts/run.py --models gemini-2.5-flash,nova-pro --conditions single_shot --scenarios S04 --repetitions 1 --output ../outputs/ablations/shared/a2_pilot --execute
```

Add `--limit 1` to execute just the first scheduled cell before inspecting it.
Resume with the same options plus `--resume`; `--limit` does not change the plan.
The frozen shuffled schedule is filtered into one sequential queue per model;
model queues run concurrently. The per-run timeout defaults to 1,200 seconds.
Five consecutive failures stop that model's queue by default. Other workers finish, then
the campaign exits unsuccessfully, preventing the suite's next ablation.

Review prompts, generated files, trace completeness, routing, read-before-write
audits, and failures before launching a larger campaign in a new output directory.
Do not pool pilot data with the main experiment if the protocol changes.

## Runtime behavior

**Ablation 1:** The runner passes the saved user prompt verbatim to
`run_opencode`, bypassing its default prompt builder. It supplies only the initial
Python file for Google/AWS conditions. The no-anchor condition starts with no
supplied Python files. As in the original experiment, OpenCode creates
`opencode.json` and `vibench_agent_prompt.md` inside each temporary workspace.
New campaigns inherit the paper's sampling policy, including GPT reasoning `none`.
The paused September 19 campaign predates this correction and is not relabeled.
Experiment metadata, condition labels, dependency inventories, and outputs stay
outside that workspace. Workspace names are random and do not encode condition.

Anchor immutability is instructed and audited, **not enforced by filesystem
permissions**. Final hashes and observed write/edit attempts are saved. Successful
anchor edits count as a failed attempt even if the final content was restored.
Read-before-generation is verified only when a successful read completes before
the assistant turn initiating the first observed Python write. Same-turn calls
do not establish exposure. Shell, subagent, or patch activity makes this check
unknown, requiring trace inspection. Such cases are retained and flagged, not
silently excluded or automatically retried until they comply.

**Ablation 2:** The agentic arm uses the archived original task and system
instructions, without a seed. The single-shot arm calls the existing LiteLLM
adapter without tools. It preserves the original task and full agent instructions
except for replacing disk-writing instructions with JSON delivery instructions
in both messages: one filename-to-Python-source mapping for all ten files. It does
not append a conflicting override. The parser
accepts bare JSON or one enclosing Markdown JSON fence, without repairing the
payload. It rejects extra/duplicate filenames, non-string contents, surrounding
commentary, and invalid JSON. The raw response is always retained.
Partial valid mappings are saved but marked incomplete. No repair LLM call is
made. Both arms inherit the original sampling policy: GPT reasoning is explicitly
`none`, while other models use provider defaults. Context/output limits, API
transports, tool access, and the output envelope can differ. This is a matched
task comparison, not isolation of every component of agency.

Ablation 1's no-anchor arm and ablation 2's agentic arm have the same inputs.
The sequential suite excludes both. Individual runners retain these conditions
for reproducibility; explicitly select only the approved new conditions. Existing
baselines are not automatically reused or double-counted by the runner.

## Saved results and resume

Each campaign has a frozen `plan.json` and `runtime.json`. Changes to prompts,
seeds, model registry, runner code, runtime versions, timeout, or the selected
cells require a new campaign rather than mixing protocols on resume.

```text
outputs/<campaign>/
  plan.json
  runtime.json
  runs/S04/nova-pro/anchor_aws/r001/attempt_001/
    input.json
    prompt.txt
    system_prompt.txt
    response.json
    trace.json              # OpenCode sessions, messages, tool parts, usage
    anchor_audit.json        # agentic only; not applicable without a seed
    opencode.json           # redacted runtime config, agentic only
    vibench_agent_prompt.md  # agentic only
    repository/             # expected Python files, including supplied seed
    metrics.json
    status.json
```

Raw response text and available OpenCode stdout/stderr are retained, not just
log tails. Trace export includes matching sessions and descendants, not unrelated
sessions. The underlying replication runner discards stdout/stderr on timeout;
the separate SQLite trace export still runs, and trace-export failures are
reported. Missing traces prevent an attempt being marked completed. Known
credential values are redacted; manually review artifacts before publication.

`--resume` skips all previously attempted cells, including failures. To make a
new attempt for failed/interrupted cells, explicitly add `--retry-failed`.
Existing attempts are never overwritten. Report first attempts as well as
retry outcomes; do not choose only successful retries for analysis.

```sh
python -B ablations/shared/summarize.py ../outputs/ablations/shared/a1_pilot
```

`metrics.json` records explicit and local-import-propagated provider attribution
separately. Supplied anchors are excluded from generated-file scores. Fractions
use all expected generated files in each group, with missing/unknown counts
reported separately; they are not silently renormalized over successes. These
are per-run descriptive measures, **not VIB estimates or confidence intervals**.
Campaign-level matched-control contrasts, run-clustered uncertainty, and
complete-run sensitivity analysis still need a frozen statistical analysis plan.

All campaign outputs are gitignored. No experiment has been launched by preparing
these runners; offline tests do not establish live provider or SDK compatibility.
