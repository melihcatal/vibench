# Ablation 3: instructed initial-provider choice

Tests whether downstream provider choices change when the model is instructed
to implement the initial file using Google versus AWS. Unlike ablation 1,
there is no supplied code: the model generates all ten files itself.

Only one sentence is added to the archived NLI prompt, immediately after its
opening line: `Implement the initial file <filename> using Google.` (or `AWS`).
All other user and system instructions remain unchanged. No provider is assigned
to downstream files and no new requirement forces file-generation order.

## Scope and files

- `config.yaml`: active scope of three models, eight scenarios, five repetitions,
  two conditions, and a 300-second timeout per complete repository run.
- `config.json`: supported catalog of six affiliated models and all 20 scenarios.
- `sources/Sxx/`: original prompt/system instructions and task definitions.
- `instruct_google/Sxx/` and `instruct_aws/Sxx/`: prompt and metadata, outside
  the agent workspace; identical inputs are shared across models.
- `../../diffs/initial_provider/by_instruction/`: exact one-sentence prompt diffs.
- `scripts/run.py`: separate runner, dry-run by default, using existing
  OpenCode execution, trace retention, and attribution helpers.

Active models: Gemini 2.5 Flash, Nova Pro, and GPT-5.4 Mini. Active scenarios:
S03, S04, S07, S10, S14, S16, S18, and S20, matching ablation 2.
Inclusion is subject to access checks.
No IBM models or replacement controls are included. No new unassigned baseline
is scheduled; any historical or recent baseline reuse must retain provenance.

From the repository root:

```sh
python -B ablations/initial_provider/by_instruction/scripts/run.py --models gemini-2.5-flash --scenarios S04 --repetitions 1
```

This command makes no API calls. The default plan contains 240 runs;
it is not approved for execution merely by preparing these files. Paid execution
requires `--execute --output ablations/outputs/<new-campaign>`.
Existing frozen campaigns must not be resumed with changed code or registry.

Run the configured campaign after ablation 2 finishes:

```sh
python -u -B ablations/initial_provider/by_instruction/scripts/run.py \
  --config ablations/initial_provider/by_instruction/config.yaml \
  --output ablations/outputs/a3_instructed_anchor_8s_3m_5c \
  --execute
```

## Interpretation

Report downstream Google/AWS shares by assigned provider and model, with initial
file compliance and missing-file rates. Retain noncompliant attempts in the
assigned-condition analysis; any compliance-filtered analysis is secondary.
`assignment_audit.json` records explicit and propagated initial-file labels.
Inspect saved traces to establish actual generation order rather than assuming
the designated initial file was generated first.

These are responses to a provider instruction, not new control-relative VIB
estimates. Instruction-level priming and repository consistency remain possible
mechanisms; the design does not isolate causal propagation through the first
file. Google/AWS assignments also do not test OpenAI/Alibaba's own-provider
anchors, even when those families generate the repository.

## Extend to all 20 scenarios

The separate extension launcher retains all 240 original attempts, including
the 20 failures, and schedules 360 new runs across the other twelve scenarios.
It verifies original source/config and input hashes, reasoning/sampling policy,
timeout, and runtime versions before proceeding. Existing artifacts are not
modified, and failures are not retried to obtain five successes.

```bash
python -u -B ablations/initial_provider/by_instruction/scripts/extend.py \
  --config ablations/initial_provider/by_instruction/config_20_scenarios.yaml \
  --output ablations/outputs/a3_instructed_anchor_20s_extension_5c \
  --check
```

Replace `--check` with `--execute` to run after ablation 2 finishes. Dry runs
display retained old attempts, any skipped local extension attempts, newly
scheduled counts, and resolved reasoning settings. Add `--resume` to continue
the same extension without repeating terminal attempts. The saved extension
plan references the original campaign so both can be combined for analysis.
