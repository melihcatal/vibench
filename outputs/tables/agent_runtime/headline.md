# Agentic runtime comparison — headline

Derived from the two evaluator reports in this directory by `ablations/snapshots/make_paper_summaries.py`.

Aligned-core VIB (percentage points), all prompt variants pooled, for the same benchmark run on two agent frameworks.

| Model | OpenCode | Agents SDK | SDK − OpenCode |
| --- | --- | --- | --- |
| `gemini-2.5-flash` | +39.2 | +37.2 | -2.0 |
| `gemini-2.5-pro` | +16.3 | +8.1 | -8.2 |
| `gpt-5.4` | +6.9 | +9.5 | +2.6 |
| `gpt-5.4-mini` | +18.2 | +14.5 | -3.7 |
| `granite-4.0-h-small` | +2.4 | +0.2 | -2.2 |
| `nova-pro` | +30.8 | +22.9 | -7.9 |
| `qwen3.6-plus` | +3.3 | -0.9 | -4.2 |

The sign of VIB agrees on both runtimes for 6 of 7 affiliated models, so the agentic finding is not an artifact of one agent framework. Magnitudes are generally smaller under the Agents SDK, which is why the paper reports OpenCode as the main arm and this as a robustness check.
