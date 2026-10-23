# Single-shot multi-file generation — runs

Tests whether the agentic gap comes from agent tooling or merely from
generating many files. The same ten-file task is produced **in one response,
without agent tools**, and compared against the paper's agentic run on the same
scenarios.

Condition: `single_shot`. Models: Gemini 2.5 Flash, GPT-5.4 Mini, Nova Pro.

| Run | Planned | Attempted | Completed | Notes |
|---|---:|---:|---:|---|
| `a2_single_shot_8s_3m_5c` | 120 | 120 | 102 | First pass, 8 scenarios. |
| `a2_single_shot_20s_extension_5c` | 180 | 180 | 147 | Extends to 12 further scenarios, retaining the 120 attempts from the first pass. |

The two together cover all 20 scenarios.

The failures matter here: a single response has to emit ten parseable files, and
some did not. That is why the result table reports both a figure over runs with
extractable output and a conservative bound that scores an unextractable run as
zero.

The comparison baseline is the paper's own agentic run, in
`../../../runs/agentic/complete/opencode_full_5c/`, not a run in this directory.

Result tables: `../../../tables/single_shot_multifile/`.
