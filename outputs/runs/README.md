# Main pipeline runs

Everything produced by `code/scripts/generation/run_direct.py` and
`run_agentic.py`. Each run directory is one execution of one config, and holds
`raw/` (the generated code) and `labeled/` (the detector's per-file provider
attribution over it).

A run's name is its path relative to this directory, and it comes from the
`name:` field of the config that produced it — so `direct/complete/full_5c`
was written by `code/configs/vibench/direct/complete/full_5c.yaml`. Re-running
that config writes back to the same place.

## complete/ — the study grid

| Run | Grid | Reported as |
|---|---|---|
| `direct/complete/full_5c` | 13 models x 20 scenarios x 4 subtasks x 3 prompt variants x 5 completions = 15,600 generations | the direct results |
| `agentic/complete/opencode_full_5c` | 10 models x 20 workflows x 2 prompt variants x 5 completions = 2,000 sessions | the agentic results |
| `agentic/complete/agents_sdk_full_5c` | 9 models, same workflow grid, on the OpenAI Agents SDK | the runtime-robustness check (paper Table 12) |

## variants/ — reduced-grid config variants

`variants/option_order/` holds the provider-option-order sweep: the same
benchmark with the affiliated provider placed first, middle, last, or omitted
from the prompt's reference list. Reduced grid — 4 affiliated models, REF
prompting, 3 completions — because the question is whether position matters, not
how large the effect is.

These are main-pipeline runs, not ablation campaigns: same runner, same
`raw/` + `labeled/` shape, different config. The four ablation campaigns, which
use their own runners, live in `../ablations/`.

Tables derived from these runs are in [`../tables/option_order/`](../tables/option_order)
and [`../tables/agent_runtime/`](../tables/agent_runtime).
