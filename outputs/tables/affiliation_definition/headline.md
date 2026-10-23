# Microsoft-OpenAI affiliation sensitivity — headline

Derived from `indirect_affiliation_sensitivity.csv` by `ablations/snapshots/make_paper_summaries.py`.

VIB for the GPT models under three affiliation definitions. `merged_microsoft_openai` is the definition used in the paper.

| Mapping | Setting | Model | VIB | 95% CI | p |
| --- | --- | --- | --- | --- | --- |
| `merged_microsoft_openai` | agentic | `gpt-5.4` | +0.069 | [+0.026, +0.111] | 0.0016 |
| `merged_microsoft_openai` | agentic | `gpt-5.4-mini` | +0.182 | [+0.137, +0.226] | 0.0002 |
| `merged_microsoft_openai` | direct | `gpt-5.4` | +0.005 (n.s.) | [-0.027, +0.037] | 0.7789 |
| `merged_microsoft_openai` | direct | `gpt-5.4-mini` | +0.079 | [+0.043, +0.115] | 0.0002 |
| `openai_only` | agentic | `gpt-5.4` | +0.023 (n.s.) | [-0.005, +0.052] | 0.1074 |
| `openai_only` | agentic | `gpt-5.4-mini` | +0.150 | [+0.111, +0.190] | 0.0002 |
| `openai_only` | direct | `gpt-5.4` | +0.036 | [+0.010, +0.064] | 0.0066 |
| `openai_only` | direct | `gpt-5.4-mini` | +0.093 | [+0.062, +0.126] | 0.0002 |
| `azure_only` | agentic | `gpt-5.4` | +0.046 | [+0.011, +0.081] | 0.0076 |
| `azure_only` | agentic | `gpt-5.4-mini` | +0.032 (n.s.) | [-0.007, +0.071] | 0.1092 |
| `azure_only` | direct | `gpt-5.4` | -0.032 | [-0.056, -0.008] | 0.0086 |
| `azure_only` | direct | `gpt-5.4-mini` | -0.015 (n.s.) | [-0.041, +0.013] | 0.3074 |

Reading the direct rows: under the merged definition GPT-5.4's direct VIB is not distinguishable from zero, while restricting attribution to OpenAI surfaces makes it significantly positive, and restricting to Azure surfaces makes it negative. Merging the two therefore dilutes the direct signal rather than creating it.
