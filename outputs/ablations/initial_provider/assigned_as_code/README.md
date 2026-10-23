# Assigned initial provider — runs

Tests whether downstream provider choices merely follow the first file. The
initial file (A1) is **supplied as existing provider-specific code**, its
provider varied, and the four downstream tasks left unchanged.

Conditions: `anchor_google`, `anchor_aws` (and `anchor_microsoft_openai` in the
sub-campaign). Models: Gemini 2.5 Flash, GPT-5.4 Mini, Nova Pro.

| Run | Planned | Attempted | Completed | Notes |
|---|---:|---:|---:|---|
| `a1_completion_20s_3m_5c` | 346 | 121 | 110 | 20 scenarios, 1200 s budget. Resumed an interrupted suite-wide execution: the 254 attempts it reused are materialised in its own `runs/` tree, verified against the `artifacts_sha256` in `plan.json`. Interrupted in turn. |
| `a1_completion_20s_3m_5c_300s` | 225 | 225 | 208 | The remaining cells at a 300 s budget, retaining 375 earlier attempts. Completes the campaign. |
| `microsoft_openai/a1_microsoft_openai_20s_3m_5c` | 300 | 76 | 57 | Separate sub-campaign adding the Microsoft/OpenAI anchor across all 20 scenarios. |

The complete campaign result is the two `a1_completion` runs together.

Because the first run absorbed its predecessor, its `plan.json` describes 346
cells while `runs/` holds attempts for 375 — the extra 254 belong to the
predecessor's plan — and `progress.json` reports the 121 it executed itself.
`retained_attempts_materialized: true` in `plan.json` records this.

Result tables: `../../../tables/assigned_as_code/`.
