# Instructed initial provider — runs

Same question as the assigned-provider campaign, but the anchor is **requested
in the prompt** rather than supplied as code: one added sentence instructing the
model to implement the initial file with a named external provider.

Conditions: `instruct_google`, `instruct_aws` (and `instruct_microsoft_openai`
in the sub-campaign). Models: Gemini 2.5 Flash, GPT-5.4 Mini, Nova Pro.

| Run | Planned | Attempted | Completed | Notes |
|---|---:|---:|---:|---|
| `a3_instructed_anchor_8s_3m_5c` | 240 | 240 | 220 | First pass, 8 scenarios. |
| `a3_instructed_anchor_20s_extension_5c` | 360 | 360 | 329 | Extends to 12 further scenarios, retaining the 240 attempts from the first pass. |
| `microsoft_openai/a3_microsoft_openai_20s_3m_5c` | 300 | 114 | 101 | Separate sub-campaign adding the Microsoft/OpenAI instruction across all 20 scenarios. |

The two `a3_` runs together cover all 20 scenarios; the extension alone covers 12.

The single added sentence is visible as a one-line diff against the paper's
original prompt in `code/ablations/diffs/initial_provider/by_instruction/`.

Result tables: `../../../tables/by_instruction/`.
