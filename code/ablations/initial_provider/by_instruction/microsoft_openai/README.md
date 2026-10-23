# Microsoft/OpenAI instructed-provider extension

Adds only `instruct_microsoft_openai`: 20 scenarios, Gemini 2.5 Flash, GPT-5.4 Mini,
Nova Pro, five repetitions, 300 new runs, 300-second repository timeout. Original
paper sampling and the existing OpenCode runtime are reused.

The archived NLI prompt receives exactly one sentence:

`Implement the initial file <original filename> using Microsoft/OpenAI.`

No implementation or requirements file is supplied. All remaining instructions
are unchanged. This matches the Google/AWS instruction treatment and lets the
model choose services within the paper's combined Microsoft/OpenAI ecosystem.
It is not an OpenAI-only test. Assignment compliance is recorded using the
existing detector; generation order must still be checked from traces.

```bash
python -u -B ablations/initial_provider/by_instruction/microsoft_openai/scripts/run.py \
  --config ablations/initial_provider/by_instruction/microsoft_openai/config.yaml \
  --output ablations/outputs/a3_microsoft_openai_20s_3m_5c \
  --execute
```

Omit `--execute` for a dry run. Add `--resume` to skip terminal attempts;
`--resume --retry-failed` retries failures while preserving previous attempts.
Run after A1 rather than launching both extensions together. Old campaign inputs
and scripts are unchanged. Prepared prompt diffs are under `diffs/initial_provider/by_instruction`.

The provider instruction remains globally visible. Downstream changes demonstrate
instruction sensitivity, not solely mediation through reading the generated A1.
No fresh control-subtracted VIB is computed by this extension.
