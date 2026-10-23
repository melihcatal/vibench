# Ablation 2: single-shot versus archived agentic generation

- Single-shot normalized artifacts are compared with archived agentic NLI on the same eight scenarios and three models; five assigned repetitions per cell.
- Provider attribution uses fractional ecosystem mass and local-import propagation. Four expected files per scored group remain in the denominator; missing/unknown files contribute zero.
- Primary unconditional shares weight scenarios equally, averaging extractable single-shot runs within scenario. Original agentic uses all assigned runs, including incomplete outputs. Zero-filled all-assigned single-shot rates are a sensitivity analysis, not observed choices for unparseable responses.
- Conditional persistence uses canonical A1 ecosystem equal to model affiliation, averages eligible repositories, and retains four downstream files per run. In single-shot outputs A1 is a designated file, not a verified earlier decision.
- Matched conditional rates restrict to scenarios with eligible runs in both settings and weight scenarios equally. Conditioning can select different runs across settings.
- 95% percentile CIs use 10,000 repository bootstrap replicates; unconditional/matched estimates resample within fixed scenario, pooled conditional estimates resample eligible runs. All four files stay together. Degenerate intervals for all-identical outcomes do not establish certainty.
- Raw responses and strict failures are preserved. Only recognized JSON-key role prefixes were removed; Python source and invalid imports were not repaired. Syntax checks are descriptive and do not filter attribution.
- No new controls: these are shares and persistence, not fresh VIB estimates. Historical date, API/runtime, output format, and 300s versus 1200s budget differences prevent an isolated causal agency claim. Nova uses its direct first-party API now versus the historical Bedrock route.
- All statistical comparisons are exploratory/descriptive; no significance or causal conclusions are drawn.

## Affiliated ecosystem shares (%)

| Model | Setting | Available / assigned | Core | Downstream | Eligible A1 | Conditional downstream |
|---|---|---:|---:|---:|---:|---:|
| gemini-2.5-flash | single_shot | 39/40 | 43.0 | 35.3 | 17 | 52.9 |
| gemini-2.5-flash | original_agentic | 40/40 | 84.4 | 83.1 | 34 | 94.9 |
| gpt-5.4-mini | single_shot | 40/40 | 30.0 | 39.4 | 12 | 95.8 |
| gpt-5.4-mini | original_agentic | 40/40 | 40.0 | 58.8 | 16 | 100.0 |
| nova-pro | single_shot | 36/40 | 20.0 | 17.0 | 7 | 80.4 |
| nova-pro | original_agentic | 40/40 | 90.0 | 63.4 | 36 | 70.5 |

## Matched eligible scenarios

| Model | Scenarios | Single-shot | Archived agentic |
|---|---|---:|---:|
| gemini-2.5-flash | S03, S04, S07, S10, S18, S20 | 55.0 | 94.2 |
| gpt-5.4-mini | S03, S04, S07, S10 | 87.5 | 100.0 |
| nova-pro | S07, S14, S16 | 67.7 | 86.7 |

## Raw A1 counts

| Model | Setting | Ecosystem counts |
|---|---|---|
| gemini-2.5-flash | single_shot | {"aws": 15, "google": 17, "microsoft_openai": 5, "unknown": 2, "unresolved": 1} |
| gemini-2.5-flash | original_agentic | {"aws": 6, "google": 34} |
| gpt-5.4-mini | single_shot | {"aws": 7, "google": 17, "independent": 2, "microsoft_openai": 12, "unknown": 2} |
| gpt-5.4-mini | original_agentic | {"aws": 6, "google": 15, "independent": 2, "microsoft_openai": 16, "unknown": 1} |
| nova-pro | single_shot | {"aws": 7, "google": 20, "microsoft_openai": 5, "unknown": 4, "unresolved": 4} |
| nova-pro | original_agentic | {"anthropic": 1, "aws": 36, "google": 1, "independent": 1, "unknown": 1} |

## Syntax audit

| Model | Files parsed | Syntax-invalid files | Runs with syntax errors |
|---|---:|---:|---:|
| gemini-2.5-flash | 390 | 7 | 4 |
| gpt-5.4-mini | 400 | 2 | 2 |
| nova-pro | 360 | 17 | 5 |

Per-run records, raw conditional mass, bootstrap intervals, strict states, missing-output sensitivities, syntax issues, and all historical prompt checks are in results.json.
