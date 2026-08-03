# Configs

Only active VIBench configs are kept here. Legacy and preliminary configs were
removed from the active workspace.

**Contents**

- [Structure](#structure)
- [Naming Convention](#naming-convention)
- [Shared Files](#shared-files)
- [Credentials](#credentials)
- [Configs Used in the Study](#configs-used-in-the-study)

## Structure

```text
configs/vibench/
├── direct/
│   ├── complete/full_5c.yaml
│   └── ablations/option_order/
│       ├── affiliated_first_3c.yaml
│       ├── affiliated_middle_3c.yaml
│       ├── affiliated_last_3c.yaml
│       └── affiliated_omitted_3c.yaml
└── agentic/
    ├── complete/
    │   ├── opencode_full_5c.yaml
    │   └── agents_sdk_full_5c.yaml
    └── ablations/option_order/
        ├── opencode/
        │   ├── affiliated_first_3c.yaml
        │   ├── affiliated_middle_3c.yaml
        │   ├── affiliated_last_3c.yaml
        │   └── affiliated_omitted_3c.yaml
        └── agents_sdk/
            ├── affiliated_first_3c.yaml
            └── affiliated_last_3c.yaml
```

Each config `name` matches the corresponding relative run path under
`outputs/runs/`. For example, `configs/vibench/direct/complete/full_5c.yaml`
writes or resumes `outputs/runs/direct/complete/full_5c`. These run names are
also how the runs appear in the published results dataset, so the config
filenames are stable identifiers and are not renamed.

## Naming Convention

- `full` — the complete study grid: every study model, all 20 scenarios or
  workflows, all prompt variants for that setting.
- `_5c` / `_3c` — completions sampled per prompt instance (5 for the main
  runs, 3 for ablations).
- `affiliated_first|middle|last|omitted` — where the model-affiliated
  provider appears in the REF reference-card list for option-order
  ablations (`omitted` removes it entirely).
- `opencode` / `agents_sdk` — the agent runtime used for agentic runs
  (OpenCode CLI vs. OpenAI Agents SDK + LiteLLM).
- Ablation configs run a reduced grid: the 4 affiliated models with the
  clearest main-run VIB signal (`gemini-2.5-flash`, `nova-pro`,
  `gpt-5.4-mini`, `granite-4.0-h-small`), REF/informed prompting only.

## Shared Files

- `configs/default.yaml`: shared runner defaults.
- `configs/.env.template`: local credential template.

## Credentials

Create `configs/.env` from the template:

```bash
cd code
cp configs/.env.template configs/.env
$EDITOR configs/.env
```

Generation scripts load `configs/.env` automatically. You only need keys for
the models selected by the config or CLI overrides.
The template also contains a few legacy/preliminary provider variables; the
VIBench configs used in the study need only the rows below.

| Model IDs | Required variables |
|---|---|
| `gemini-2.5-pro`, `gemini-2.5-flash` | `GEMINI_API_KEY` |
| `gpt-5.4`, `gpt-5.4-mini` | `OPENAI_API_KEY` |
| `grok-4-1-fast-reasoning` | `XAI_API_KEY`, `XAI_API_BASE` |
| `nova-pro`, `nova-2-lite` | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION_NAME` |
| `qwen3.6-plus`, `qwen3-coder-flash` | `DASHSCOPE_API_KEY`, `DASHSCOPE_BASE_URL` |
| `granite-4.0-h-small` | `WATSONX_API_KEY`, `WATSONX_PROJECT_ID`, `WATSONX_URL` |
| `deepseek-v3.2` | `DEEPSEEK_API_KEY` |
| `mistral-large-3` | `MISTRAL_API_KEY` |
| `granite-4.0-h-tiny-local` | `LOCAL_MLX_API_KEY`, `LOCAL_MLX_TINY_API_BASE`, plus a local `mlx_lm.server` endpoint |

OpenCode agentic runs for `nova-pro` and `granite-4.0-h-small` also require
local LiteLLM proxies because OpenCode does not use those provider routes
directly in this package:

```bash
scripts/generation/start_litellm_proxies.sh
```

Keep that helper running in a separate terminal while
`scripts/generation/run_agentic.py` runs. The helper sources `configs/.env` and
serves the OpenCode-compatible aliases `nova-pro` and `granite-4.0-h-small`.

## Configs Used in the Study

- `direct/complete/full_5c.yaml`: all study direct models, 20 scenarios,
  4 subtasks per scenario, NLI/FIM/REF (`reference_open`) prompting, 5
  completions per prompt, 15,600 expected generations.
- `agentic/complete/opencode_full_5c.yaml`: study OpenCode agentic setting,
  10 models, 20 workflows, `free` and `informed` variants, 5 completions per
  workflow, 2,000 expected sessions.
- `agentic/complete/agents_sdk_full_5c.yaml`: OpenAI Agents SDK runtime check,
  9 active models, 20 workflows, `free` and `informed` variants, 5 completions
  per workflow, 1,800 expected sessions. `deepseek-v3.2` is commented out in
  that config because it did not complete the full Agents SDK run reliably.
- `direct/ablations/option_order/affiliated_{first,middle,last,omitted}_3c.yaml`:
  option-order ablations for the direct REF setting (Appendix A.4.1). 4
  affiliated models, 20 scenarios, 4 subtasks, `reference_open` only, 3
  completions, 960 expected generations per config.
- `agentic/ablations/option_order/opencode/affiliated_{first,middle,last,omitted}_3c.yaml`:
  option-order ablations for the agentic `informed` setting on the primary
  OpenCode runtime (Appendix A.4.2). 4 affiliated models, 20 workflows,
  `informed` variant only, 3 completions per config.
- `agentic/ablations/option_order/agents_sdk/affiliated_{first,last}_3c.yaml`:
  option-order ablations for the agentic `informed` setting on the Agents SDK
  runtime (Appendix A.4.2, runtime check). 4 affiliated models, 20 workflows,
  `informed` variant only, 3 completions, 240 expected sessions per config.

For agentic runs, `free` corresponds to the NLI-style task prompt and
`informed` corresponds to the REF-style prompt with documented provider
alternatives.

All active configs leave `temperature`, `top_p`, and `max_tokens` unset unless
a provider route requires a specific override. GPT-5.4-family reasoning is
explicitly disabled where the route supports a `none` control; other models use
provider defaults because no universal cross-provider reasoning knob exists.
