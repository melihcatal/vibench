# Full versus staged task disclosure — runs

Tests whether downstream persistence is advance planning. Files are generated
**one per request, A1 first, each in a fresh conversation**, revealing either
the whole task list (`full_disclosure`) or only the current task
(`staged_disclosure`). Logs and file snapshots verify the generation order.

Models: Gemini 2.5 Flash, GPT-5.4 Mini, Nova Pro.

| Run | Planned | Attempted | Completed | Notes |
|---|---:|---:|---:|---|
| `a4_disclosure_6s_3m_5c` | 180 | 43 | 32 | First pass, 6 scenarios at a 1200 s budget. Interrupted — ten sequential requests per run makes this the slowest campaign. |
| `a4_disclosure_6s_3m_5c_300s` | 12 | 12 | 8 | Nova Pro only, at a 300 s budget, retaining 168 earlier attempts. |
| `a4_disclosure_20s_extension_3m_5c` | 420 | 102 | 75 | Extends to 14 further scenarios at a 300 s budget. |

Each cell here is ten separate model requests rather than one agent session,
which is why the attempt counts are low relative to what was planned and why
the campaign is by far the largest on disk.

Both conditions share the same first file, so the contrast isolates whether the
forward task list was visible. That removal is visible as a diff in
`code/ablations/diffs/agentic_mechanism/task_disclosure/`.

Result tables: `../../../tables/task_disclosure/`,
which report the `first_attempt` scope as the paper does, alongside
`latest_finished_attempt`.
