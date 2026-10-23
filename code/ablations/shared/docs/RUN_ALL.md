# Full ablation suite

Run from `code/`. Campaign outputs are written under `../outputs/ablations/`.

Run from `code/` with the project's Python environment activated.
API credentials are loaded from `code/configs/.env`; do not put them in commands.

```bash
conda activate vibench
bash ablations/run_all.sh ../outputs/ablations/shared/full_suite_5reps
```

That command validates all four plans without generation. To execute:

```bash
bash ablations/run_all.sh ../outputs/ablations/shared/full_suite_5reps --execute
```

Models run in parallel within an ablation. Ablations execute strictly 1, 2, 3, 4;
no next stage starts until the previous stage succeeds. Ablation 1 defaults to
six models, 20 scenarios and five repetitions. Ablations 2 and 3 select three models,
eight scenarios, five repetitions, and a 300-second timeout. Ablation 4
uses `agentic_mechanism/task_disclosure/config.yaml`: three models, six scenarios, five repetitions.
Override with `--models`, `--scenarios`, `--repetitions`, or `--workers` when needed.

| Ablation | Conditions | Runs |
|---|---|---:|
| 1 | Supplied Google / AWS initial file | 1,200 |
| 2 | Single-shot ten-file response | 120 |
| 3 | Instructed Google / AWS initial provider | 240 |
| 4 | Full / staged disclosure, fresh session per file | 180 |
| Total | | 1,740 |

Ablation 4 alone contains 1,800 file requests; each can involve additional tool
turns. Runtime and cost depend on model behavior. No controls, no-anchor runs, or
duplicated original-agentic baselines are newly scheduled. Full-disclosure in
ablation 4 is a new matched baseline, not the historical agentic condition.
Use its standalone runner to run only ablation 4; this suite still schedules all
four stages. Explicit suite scope flags apply to every stage and can expand the
targeted ablation-4 scope, so inspect the printed dry-run counts first.

Progress bars show totals and individual models. Each stage writes `progress.json`,
`logs/<model>.jsonl`, immutable `plan.json`/`runtime.json`, and all attempts under
`runs/`. Five consecutive errors stop that model's queue; other model queues can
finish, but the suite then stops before starting the next ablation. Failures and
partial artifacts are retained. Quota errors never trigger an infinite retry loop.

Resume an unchanged campaign with the same scope:

```bash
bash ablations/run_all.sh ../outputs/ablations/shared/full_suite_5reps --execute --resume
```

Previously failed attempts need an explicit `--retry-failed`; otherwise they
remain unresolved and prevent advancement. Retried attempts get new directories.
Changed code, input hashes, SDK runtime versions, or registry settings require a
new campaign directory. Do not edit source while the suite is running. The old
September 18 partial campaigns cannot be resumed with these revised manifests.
The paused `full_suite_20260919` campaign retains its original ten-repetition plan
and outputs. The five-repetition defaults do not rewrite or resume that campaign;
its source hashes differ, so existing results need an explicit continuation plan.

S11's Google anchor now uses `google-genai` in Vertex mode; migration metadata
preserves the historical evidence label. All 40 anchors have offline syntax,
attribution, and mocked request/response contract tests. They are generated-code
context, not a claim of live cloud execution or identical service semantics.
Provisioning assumptions and provider differences are in each anchor contract.

All ablations inherit sampling from the original paper YAML files using the
original loaders. GPT reasoning is explicitly `none` in both the OpenCode and
direct adapters; other models retain provider defaults. Original sampling YAMLs
and per-ablation scope YAMLs are hashed into the plan. Each attempt also saves
`sampling_audit.json` with resolved settings and recorded reasoning usage.

The new experiment wrappers, templates, and launch scripts live under
`ablations/`. Runtime/route differences from archived runs are documented
in `SETTINGS_AUDIT.md`; this is not a claim of an identical historical runtime.
