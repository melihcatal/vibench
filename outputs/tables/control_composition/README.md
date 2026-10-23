# Control-Baseline Dispersion Audit

Audited `500` scenario × prompt-setting × target-ecosystem cells.
Rates use the same share-normalized ecosystem attribution as VIB.

## Panel A: Aggregation-Rule Sensitivity

VIB values are percentage points. `Pooled` weights control generations directly; `Median` uses the scenario-specific median control rate.

| Setting | Model | Mean | Pooled | Median | Pooled - Mean | Median - Mean |
|---|---|---:|---:|---:|---:|---:|
| direct | gemini-2.5-flash | +18.79 | +18.79 | +17.25 | +0.00 | -1.54 |
| direct | gemini-2.5-pro | -4.46 | -4.46 | -6.00 | -0.00 | -1.54 |
| direct | gpt-5.4 | +0.46 | +0.46 | +1.04 | -0.00 | +0.58 |
| direct | gpt-5.4-mini | +7.88 | +7.88 | +8.46 | -0.00 | +0.58 |
| direct | granite-4.0-h-small | +2.94 | +2.94 | +3.12 | +0.00 | +0.19 |
| direct | granite-4.0-h-tiny-local | +2.56 | +2.56 | +2.75 | +0.00 | +0.19 |
| direct | nova-2-lite | -13.81 | -13.81 | -12.96 | +0.00 | +0.85 |
| direct | nova-pro | +12.23 | +12.23 | +13.08 | +0.00 | +0.85 |
| direct | qwen3-coder-flash | +3.06 | +3.06 | +3.08 | +0.00 | +0.03 |
| direct | qwen3.6-plus | -0.03 | -0.03 | +0.00 | +0.00 | +0.03 |
| agentic | gemini-2.5-flash | +39.21 | +39.21 | +37.75 | +0.00 | -1.46 |
| agentic | gemini-2.5-pro | +16.33 | +16.33 | +14.88 | +0.00 | -1.46 |
| agentic | gpt-5.4 | +6.86 | +6.86 | +7.88 | +0.00 | +1.01 |
| agentic | gpt-5.4-mini | +18.17 | +18.17 | +19.19 | +0.00 | +1.01 |
| agentic | granite-4.0-h-small | +2.38 | +2.38 | +3.25 | +0.00 | +0.88 |
| agentic | nova-pro | +30.80 | +30.80 | +31.02 | +0.00 | +0.22 |
| agentic | qwen3.6-plus | +3.27 | +3.27 | +3.94 | +0.00 | +0.67 |

## Panel B: Exhaustive Control-Subset Sensitivity

All seven non-empty subsets are included: three singleton controls, three control pairs, and all three controls.

| Setting | Model | Strict | Min | Median | Max | Positive | Negative |
|---|---|---:|---:|---:|---:|---:|---:|
| direct | gemini-2.5-flash | +18.79 | +13.29 | +18.79 | +28.07 | 7/7 | 0/7 |
| direct | gemini-2.5-pro | -4.46 | -9.96 | -4.46 | +4.82 | 1/7 | 6/7 |
| direct | gpt-5.4 | +0.46 | -1.08 | +0.46 | +1.79 | 5/7 | 2/7 |
| direct | gpt-5.4-mini | +7.87 | +6.33 | +7.87 | +9.21 | 7/7 | 0/7 |
| direct | granite-4.0-h-small | +2.94 | +2.74 | +2.94 | +3.12 | 7/7 | 0/7 |
| direct | granite-4.0-h-tiny-local | +2.56 | +2.36 | +2.56 | +2.75 | 7/7 | 0/7 |
| direct | nova-2-lite | -13.81 | -20.43 | -13.81 | -3.62 | 0/7 | 7/7 |
| direct | nova-pro | +12.23 | +5.61 | +12.23 | +22.42 | 7/7 | 0/7 |
| direct | qwen3-coder-flash | +3.06 | +2.83 | +3.06 | +3.25 | 7/7 | 0/7 |
| direct | qwen3.6-plus | -0.03 | -0.25 | -0.03 | +0.17 | 2/7 | 4/7 |
| agentic | gemini-2.5-flash | +39.21 | +29.62 | +39.21 | +53.62 | 7/7 | 0/7 |
| agentic | gemini-2.5-pro | +16.33 | +6.75 | +16.33 | +30.75 | 7/7 | 0/7 |
| agentic | gpt-5.4 | +6.86 | +1.52 | +6.86 | +11.81 | 7/7 | 0/7 |
| agentic | gpt-5.4-mini | +18.17 | +12.83 | +18.17 | +23.12 | 7/7 | 0/7 |
| agentic | granite-4.0-h-small | +2.38 | +0.25 | +2.38 | +3.75 | 7/7 | 0/7 |
| agentic | nova-pro | +30.80 | +24.75 | +30.80 | +40.06 | 7/7 | 0/7 |
| agentic | qwen3.6-plus | +3.27 | +1.56 | +3.27 | +4.44 | 7/7 | 0/7 |

## Panel C: Scenario-Level Influence

- Median range across the three controls: **5.0%**.
- Median maximum leave-one-out change in the mean baseline: **1.7%**.
- 90th percentile maximum leave-one-out change: **17.5%**.
- Maximum leave-one-out change: **33.3%**.
- Cells with leave-one-out change ≥5 pp: **200/500**.
- Cells with leave-one-out change ≥10 pp: **111/500**.

Among cells where at least one control selects the target ecosystem:
- Active cells: **268/500**.
- Median control range: **25.0%**.
- Median maximum leave-one-out change: **8.3%**.
- Active cells with leave-one-out change ≥10 pp: **111/268**.

### Most Sensitive Cells

| Setting | Scenario | Target | DeepSeek | Mistral | Grok | Mean | Range | Max LOO change | Removed |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| direct_fim | S03 | aws | 100.0% | 0.0% | 0.0% | 33.3% | 100.0% | 33.3% | deepseek-v3.2 |
| agentic_free | S15 | microsoft_openai | 0.0% | 100.0% | 0.0% | 33.3% | 100.0% | 33.3% | mistral-large-3 |
| direct_fim | S10 | microsoft_openai | 100.0% | 5.0% | 95.0% | 66.7% | 95.0% | 30.8% | mistral-large-3 |
| direct_reference_open | S16 | aws | 10.0% | 0.0% | 97.5% | 35.8% | 97.5% | 30.8% | grok-4-1-fast-reasoning |
| agentic_free | S03 | google | 100.0% | 95.0% | 5.0% | 66.7% | 95.0% | 30.8% | grok-4-1-fast-reasoning |
| agentic_informed | S20 | google | 100.0% | 80.0% | 0.0% | 60.0% | 100.0% | 30.0% | grok-4-1-fast-reasoning |
| direct_nli | S07 | microsoft_openai | 95.0% | 95.0% | 5.0% | 65.0% | 90.0% | 30.0% | grok-4-1-fast-reasoning |
| direct_fim | S17 | google | 0.0% | 90.0% | 1.7% | 30.6% | 90.0% | 29.7% | mistral-large-3 |
| direct_fim | S17 | aws | 100.0% | 10.0% | 96.7% | 68.9% | 90.0% | 29.4% | mistral-large-3 |
| agentic_free | S05 | google | 100.0% | 75.0% | 0.0% | 58.3% | 100.0% | 29.2% | grok-4-1-fast-reasoning |
| direct_nli | S02 | google | 75.0% | 5.0% | 100.0% | 60.0% | 95.0% | 27.5% | mistral-large-3 |
| agentic_free | S15 | aws | 100.0% | 0.0% | 60.0% | 53.3% | 100.0% | 26.7% | mistral-large-3 |
| agentic_informed | S19 | google | 100.0% | 60.0% | 0.0% | 53.3% | 100.0% | 26.7% | grok-4-1-fast-reasoning |
| direct_fim | S20 | aws | 85.0% | 0.0% | 10.0% | 31.7% | 85.0% | 26.7% | deepseek-v3.2 |
| agentic_informed | S20 | aws | 0.0% | 0.0% | 80.0% | 26.7% | 80.0% | 26.7% | grok-4-1-fast-reasoning |
| agentic_free | S19 | google | 100.0% | 100.0% | 20.0% | 73.3% | 80.0% | 26.7% | grok-4-1-fast-reasoning |
| agentic_informed | S01 | aws | 20.0% | 20.0% | 100.0% | 46.7% | 80.0% | 26.7% | grok-4-1-fast-reasoning |
| agentic_free | S04 | google | 60.0% | 92.5% | 0.0% | 50.8% | 92.5% | 25.4% | grok-4-1-fast-reasoning |
| direct_nli | S04 | google | 100.0% | 50.0% | 0.0% | 50.0% | 100.0% | 25.0% | deepseek-v3.2 |
| direct_nli | S16 | aws | 40.0% | 10.0% | 100.0% | 50.0% | 90.0% | 25.0% | grok-4-1-fast-reasoning |
