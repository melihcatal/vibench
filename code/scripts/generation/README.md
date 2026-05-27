# Generation Scripts

Run all commands from the `code/` directory.

```bash
cd code
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp configs/.env.template configs/.env
$EDITOR configs/.env
```

The runners load credentials from `configs/.env`. Fill only the keys for the
models you actually run. The full direct config used in the study also includes
`granite-4.0-h-tiny-local`, which requires a local OpenAI-compatible MLX server;
exclude that model with `--model ...` if you cannot serve it locally.
The key-to-model mapping is listed in `configs/README.md`.

**Contents**

- [Runners](#runners)
- [Output Names](#output-names)
- [Direct Generation](#direct-generation)
- [OpenCode Agentic Generation](#opencode-agentic-generation)
- [OpenAI Agents SDK Agentic Generation](#openai-agents-sdk-agentic-generation)
- [Single-Model Reruns](#single-model-reruns)
- [Resume Canonical Runs](#resume-canonical-runs)
- [Evaluate New Generations](#evaluate-new-generations)
- [Ablations](#ablations)
- [Makefile Wrappers](#makefile-wrappers)

## Runners

- `run_direct.py`: direct single-file benchmark runner.
- `run_agentic.py`: OpenCode multi-file agentic runner.
- `run_agentic_litellm_agents.py`: OpenAI Agents SDK + LiteLLM multi-file
  agentic runner with an explicit `write_file` tool.
- `start_litellm_proxies.sh`: starts the local LiteLLM proxies required by the
  OpenCode runner for Nova Pro and Granite H-Small.

Both agentic runners use `benchmark/vibench/agentic/tasks.jsonl`.

## Output Names

The YAML `name` field is the canonical run path under `outputs/runs/`. To avoid
modifying bundled paper outputs, use `--name scratch/...` or `--name reruns/...`
for new generations. Use `--resume <run_id>` only when you intentionally want to
continue or retry an existing run directory.

## Direct Generation

Smoke test one Gemini completion per S18 direct subtask. This makes four API
calls because each direct scenario has four subtasks:

```bash
python scripts/generation/run_direct.py \
  --config configs/vibench/direct/complete/full_5c.yaml \
  --name scratch/direct_gemini_s18_nli \
  --model gemini-2.5-flash \
  --scenario S18 \
  --modality nli \
  --completions 1 \
  --sequential \
  -v
```

Run the full direct setting used in the study into a new run directory:

```bash
python scripts/generation/run_direct.py \
  --config configs/vibench/direct/complete/full_5c.yaml \
  --name reruns/direct_full_5c \
  --skip-from both \
  --retry-errors \
  --retry-empty
```

The direct config used in the study uses:

- 13 models
- 20 provider-selectable VIBench scenarios
- 4 subtasks per scenario
- 3 prompt variants: `nli`, `fim`, `reference_open`
- 5 completions per prompt
- 15,600 expected generations

## OpenCode Agentic Generation

Install the OpenCode CLI separately and verify it is on `PATH`:

```bash
opencode --version
```

For the full OpenCode config, keep a separate terminal open for the LiteLLM
proxies used by Nova Pro and Granite H-Small:

```bash
cd code
scripts/generation/start_litellm_proxies.sh
```

This helper sources `configs/.env` and starts:

- Bedrock proxy on `http://127.0.0.1:4000/v1` with alias `nova-pro`
- watsonx proxy on `http://127.0.0.1:4001/v1` with alias
  `granite-4.0-h-small`

Smoke test one Gemini OpenCode agentic run without needing those proxies:

```bash
python scripts/generation/run_agentic.py \
  --config configs/vibench/agentic/complete/opencode_full_5c.yaml \
  --name scratch/opencode_gemini_s18_free \
  --model gemini-2.5-flash \
  --task S18 \
  --variant free \
  --completions 1 \
  --sequential \
  -v
```

Run the full OpenCode setting used in the study into a new run directory:

```bash
python scripts/generation/run_agentic.py \
  --config configs/vibench/agentic/complete/opencode_full_5c.yaml \
  --name reruns/agentic_opencode_full_5c \
  --retry-errors \
  --retry-empty \
  --retry-incomplete
```

The OpenCode config used in the study uses:

- 10 agentic-capable models
- 20 VIBench agentic workflows
- 2 prompt variants: `free` (NLI-style) and `informed` (REF-style)
- 5 completions per workflow
- 10 expected Python files per workflow
- GPT-5.4-family OpenCode variant `none` where supported
- 2,000 expected sessions

## OpenAI Agents SDK Agentic Generation

This runtime does not use the OpenCode CLI. It routes model calls through
LiteLLM inside the Python process and writes files through an explicit
`write_file` tool.

Smoke test:

```bash
python scripts/generation/run_agentic_litellm_agents.py \
  --config configs/vibench/agentic/complete/agents_sdk_full_5c.yaml \
  --name scratch/agents_sdk_gemini_s18_free \
  --model gemini-2.5-flash \
  --task S18 \
  --variant free \
  --completions 1 \
  --sequential \
  -v
```

Full Agents SDK runtime check used in the study:

```bash
python scripts/generation/run_agentic_litellm_agents.py \
  --config configs/vibench/agentic/complete/agents_sdk_full_5c.yaml \
  --name reruns/agentic_agents_sdk_full_5c \
  --retry-errors \
  --retry-empty \
  --retry-incomplete
```

The Agents SDK config used in the study has 9 active models and schedules 1,800
sessions. `deepseek-v3.2` is left commented in that config because it did not
complete the full Agents SDK run reliably.

## Single-Model Reruns

To use the configs from the study but restrict execution to one model, add
`--model <model-id>` and write to a separate `reruns/...` name:

```bash
python scripts/generation/run_direct.py \
  --config configs/vibench/direct/complete/full_5c.yaml \
  --name reruns/direct_gpt-5.4-mini_full_5c \
  --model gpt-5.4-mini \
  --skip-from both \
  --retry-errors \
  --retry-empty

python scripts/generation/run_agentic.py \
  --config configs/vibench/agentic/complete/opencode_full_5c.yaml \
  --name reruns/agentic_opencode_gpt-5.4-mini_full_5c \
  --model gpt-5.4-mini \
  --retry-errors \
  --retry-empty \
  --retry-incomplete

python scripts/generation/run_agentic_litellm_agents.py \
  --config configs/vibench/agentic/complete/agents_sdk_full_5c.yaml \
  --name reruns/agentic_agents_sdk_gpt-5.4-mini_full_5c \
  --model gpt-5.4-mini \
  --retry-errors \
  --retry-empty \
  --retry-incomplete
```

Expected sizes for one-model study-config reruns are 1,200 direct generations and
200 OpenCode agentic sessions. The Agents SDK one-model target also schedules
200 sessions when the selected model is active in that config.

## Resume Canonical Runs

The bundled canonical run IDs are:

- `direct/complete/full_5c`
- `agentic/complete/opencode_full_5c`
- `agentic/complete/agents_sdk_full_5c`

Use `--resume` only for deliberate continuation or retries:

```bash
python scripts/generation/run_direct.py \
  --config configs/vibench/direct/complete/full_5c.yaml \
  --resume direct/complete/full_5c \
  --skip-from both \
  --retry-errors \
  --retry-empty

python scripts/generation/run_agentic.py \
  --config configs/vibench/agentic/complete/opencode_full_5c.yaml \
  --resume agentic/complete/opencode_full_5c \
  --retry-errors \
  --retry-empty \
  --retry-incomplete
```

## Evaluate New Generations

After generating raw outputs, run the detector/evaluator to create labeled
outputs and reports:

```bash
python scripts/evaluation/evaluate.py \
  --run reruns/direct_full_5c \
  --format md \
  --output outputs/runs/reruns/direct_full_5c/report.md

python scripts/evaluation/evaluate_agentic.py \
  --run reruns/agentic_opencode_full_5c \
  --direct-run reruns/direct_full_5c
```

For agentic-only smoke tests, you can pair against the bundled direct run:

```bash
python scripts/evaluation/evaluate_agentic.py \
  --run scratch/opencode_gemini_s18_free \
  --direct-run direct/complete/full_5c
```

## Ablations

Option-order and affiliated-omission robustness configs live under:

- `configs/vibench/direct/ablations/option_order/`
- `configs/vibench/agentic/ablations/option_order/opencode/`
- `configs/vibench/agentic/ablations/option_order/agents_sdk/`

The convenience wrapper is:

```bash
scripts/generation/run_extended_ablations.sh --help
```

## Makefile Wrappers

The Python scripts above are the canonical interface. The `code/Makefile`
provides shorter optional wrappers for common smoke checks and full reruns:

```bash
make gen-smoke-all GEN_MODEL=gpt-5.4-mini
make gen-smoke-direct GEN_MODEL=gpt-5.4-mini GEN_SCENARIO=S18
make gen-smoke-opencode GEN_MODEL=gpt-5.4-mini GEN_TASK=S18 GEN_VARIANT=both
make gen-smoke-agents-sdk GEN_MODEL=gpt-5.4-mini GEN_TASK=S18 GEN_VARIANT=both

make gen-model-all GEN_MODEL=gpt-5.4-mini
make gen-direct-model GEN_MODEL=gpt-5.4-mini
make gen-opencode-model GEN_MODEL=gpt-5.4-mini
make gen-agents-sdk-model GEN_MODEL=gpt-5.4-mini

make gen-proxies          # needed for OpenCode Nova/Granite full runs
make gen-direct-full
make gen-opencode-full
make gen-agents-sdk-full
```

Useful variables:

- `GEN_MODEL`: model id, default `gpt-5.4-mini`
- `GEN_SCENARIO`: direct smoke scenario, default `S18`
- `GEN_TASK`: agentic smoke workflow, default `$(GEN_SCENARIO)`
- `GEN_VARIANT`: agentic prompt variant, default `both`
- `GEN_COMPLETIONS`: completions per prompt/workflow, default `1`
- `GEN_RUN_ROOT`: output root for smoke runs, default `scratch/smoke_<timestamp>`
- `GEN_DIRECT_MODEL_RUN`, `GEN_OPENCODE_MODEL_RUN`,
  `GEN_AGENTS_SDK_MODEL_RUN`: output run IDs for one-model study-config reruns
