# Per-Model Gini and VIB

Values are point estimates with 95% bootstrap confidence intervals. GI is computed at ecosystem level and averaged over scenarios; its CI resamples scenarios. VIB uses the paper's scenario-matched response bootstrap. Control-model VIB is undefined by design.

## Direct

| Model | Role | Affiliation | Scenarios | VIB pp [95% CI] | Mean GI [95% CI] | Mean normalized GI [95% CI] |
|---|---|---|---:|---:|---:|---:|
| deepseek-v3.2 | control | n/a | 20 | n/a | 0.610 [0.555, 0.665] | 0.743 [0.675, 0.806] |
| gemini-2.5-flash | affiliated | google | 20 | 18.787 [16.009, 21.616] | 0.653 [0.611, 0.688] | 0.795 [0.747, 0.833] |
| gemini-2.5-pro | affiliated | google | 20 | -4.463 [-7.014, -2.074] | 0.612 [0.559, 0.662] | 0.746 [0.684, 0.807] |
| gpt-5.4 | affiliated | microsoft_openai | 20 | 0.458 [-1.542, 2.542] | 0.637 [0.582, 0.690] | 0.775 [0.712, 0.838] |
| gpt-5.4-mini | affiliated | microsoft_openai | 20 | 7.875 [5.708, 10.181] | 0.597 [0.537, 0.662] | 0.726 [0.661, 0.798] |
| granite-4.0-h-small | affiliated | ibm | 20 | 2.935 [1.991, 3.917] | 0.605 [0.559, 0.639] | 0.739 [0.684, 0.786] |
| granite-4.0-h-tiny-local | affiliated | ibm | 20 | 2.560 [1.648, 3.505] | 0.566 [0.505, 0.631] | 0.687 [0.611, 0.760] |
| grok-4-1-fast-reasoning | control | n/a | 20 | n/a | 0.682 [0.633, 0.729] | 0.830 [0.767, 0.887] |
| mistral-large-3 | control | n/a | 20 | n/a | 0.632 [0.588, 0.675] | 0.770 [0.714, 0.821] |
| nova-2-lite | affiliated | aws | 20 | -13.810 [-15.718, -11.926] | 0.622 [0.578, 0.664] | 0.759 [0.704, 0.810] |
| nova-pro | affiliated | aws | 20 | 12.231 [9.773, 14.620] | 0.593 [0.526, 0.656] | 0.721 [0.642, 0.796] |
| qwen3-coder-flash | affiliated | alibaba | 20 | 3.056 [2.167, 4.028] | 0.603 [0.551, 0.646] | 0.737 [0.673, 0.799] |
| qwen3.6-plus | affiliated | alibaba | 20 | -0.028 [-0.333, 0.306] | 0.673 [0.621, 0.727] | 0.820 [0.760, 0.879] |

## Agentic

| Model | Role | Affiliation | Scenarios | VIB pp [95% CI] | Mean GI [95% CI] | Mean normalized GI [95% CI] |
|---|---|---|---:|---:|---:|---:|
| deepseek-v3.2 | control | n/a | 20 | n/a | 0.673 [0.623, 0.720] | 0.826 [0.769, 0.882] |
| gemini-2.5-flash | affiliated | google | 20 | 39.208 [36.208, 42.104] | 0.723 [0.681, 0.765] | 0.888 [0.841, 0.933] |
| gemini-2.5-pro | affiliated | google | 20 | 16.333 [13.437, 19.271] | 0.713 [0.673, 0.750] | 0.876 [0.831, 0.921] |
| gpt-5.4 | affiliated | microsoft_openai | 20 | 6.861 [4.423, 9.084] | 0.697 [0.660, 0.732] | 0.856 [0.814, 0.898] |
| gpt-5.4-mini | affiliated | microsoft_openai | 20 | 18.174 [15.597, 20.708] | 0.654 [0.595, 0.713] | 0.800 [0.733, 0.864] |
| granite-4.0-h-small | affiliated | ibm | 20 | 2.375 [1.000, 3.813] | 0.505 [0.442, 0.574] | 0.620 [0.544, 0.693] |
| grok-4-1-fast-reasoning | control | n/a | 20 | n/a | 0.655 [0.589, 0.717] | 0.804 [0.725, 0.881] |
| mistral-large-3 | control | n/a | 20 | n/a | 0.570 [0.528, 0.612] | 0.700 [0.651, 0.755] |
| nova-pro | affiliated | aws | 20 | 30.799 [27.631, 34.001] | 0.542 [0.489, 0.597] | 0.669 [0.593, 0.742] |
| qwen3.6-plus | affiliated | alibaba | 20 | 3.271 [2.020, 4.521] | 0.710 [0.667, 0.748] | 0.873 [0.821, 0.922] |
