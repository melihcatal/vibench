# Gini Index Across Prompt Settings

Paper-style scenario-wide provider universes are computed independently within each setting.
Agentic results use `aligned_core` components; multi-label counting is `occurrence`.
Agentic `free` corresponds to NLI-style prompting and `informed` to Reference-Open-style prompting; there is no agentic FIM condition.

## Setting-Level Results

Raw GI has scenario-specific maximum `(n-1)/n`; normalized GI divides by this maximum and ranges from 0 to 1.

| Setting | Valid / total | Mean GI | Median GI | Mean normalized | Median normalized | Min | Max |
|---|---:|---:|---:|---:|---:|---:|---:|
| direct_nli | 258 / 260 | 0.591 | 0.623 | 0.792 | 0.805 | 0.167 | 0.833 |
| direct_fim | 258 / 260 | 0.597 | 0.625 | 0.798 | 0.833 | 0.075 | 0.800 |
| direct_reference_open | 260 / 260 | 0.616 | 0.642 | 0.761 | 0.800 | 0.180 | 0.857 |
| agentic_free | 200 / 200 | 0.619 | 0.667 | 0.838 | 0.900 | 0.000 | 0.800 |
| agentic_informed | 200 / 200 | 0.623 | 0.667 | 0.777 | 0.863 | 0.000 | 0.833 |

## Model-Level Results

| Setting | Model | Scenarios | Mean GI | Median GI | Mean normalized | Median normalized | Min | Max |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| direct_nli | deepseek-v3.2 | 20 | 0.588 | 0.617 | 0.784 | 0.800 | 0.267 | 0.800 |
| direct_nli | gemini-2.5-flash | 20 | 0.596 | 0.628 | 0.793 | 0.837 | 0.333 | 0.750 |
| direct_nli | gemini-2.5-pro | 20 | 0.545 | 0.533 | 0.731 | 0.800 | 0.220 | 0.760 |
| direct_nli | gpt-5.4 | 20 | 0.584 | 0.633 | 0.784 | 0.834 | 0.275 | 0.800 |
| direct_nli | gpt-5.4-mini | 20 | 0.541 | 0.506 | 0.722 | 0.691 | 0.233 | 0.800 |
| direct_nli | granite-4.0-h-small | 20 | 0.563 | 0.547 | 0.752 | 0.721 | 0.333 | 0.724 |
| direct_nli | granite-4.0-h-tiny-local | 18 | 0.608 | 0.667 | 0.823 | 0.833 | 0.167 | 0.800 |
| direct_nli | grok-4-1-fast-reasoning | 20 | 0.626 | 0.655 | 0.840 | 0.837 | 0.425 | 0.750 |
| direct_nli | mistral-large-3 | 20 | 0.634 | 0.629 | 0.849 | 0.867 | 0.400 | 0.833 |
| direct_nli | nova-2-lite | 20 | 0.636 | 0.667 | 0.850 | 0.873 | 0.278 | 0.800 |
| direct_nli | nova-pro | 20 | 0.492 | 0.461 | 0.657 | 0.646 | 0.250 | 0.760 |
| direct_nli | qwen3-coder-flash | 20 | 0.639 | 0.667 | 0.857 | 0.890 | 0.367 | 0.800 |
| direct_nli | qwen3.6-plus | 20 | 0.637 | 0.658 | 0.855 | 0.867 | 0.425 | 0.760 |
| direct_fim | deepseek-v3.2 | 20 | 0.651 | 0.667 | 0.872 | 0.900 | 0.475 | 0.800 |
| direct_fim | gemini-2.5-flash | 20 | 0.598 | 0.613 | 0.801 | 0.812 | 0.375 | 0.800 |
| direct_fim | gemini-2.5-pro | 20 | 0.557 | 0.562 | 0.742 | 0.758 | 0.275 | 0.780 |
| direct_fim | gpt-5.4 | 20 | 0.551 | 0.627 | 0.736 | 0.810 | 0.075 | 0.750 |
| direct_fim | gpt-5.4-mini | 20 | 0.542 | 0.541 | 0.724 | 0.758 | 0.250 | 0.750 |
| direct_fim | granite-4.0-h-small | 20 | 0.535 | 0.564 | 0.718 | 0.752 | 0.191 | 0.800 |
| direct_fim | granite-4.0-h-tiny-local | 18 | 0.711 | 0.750 | 0.950 | 1.000 | 0.500 | 0.800 |
| direct_fim | grok-4-1-fast-reasoning | 20 | 0.607 | 0.658 | 0.811 | 0.883 | 0.318 | 0.750 |
| direct_fim | mistral-large-3 | 20 | 0.608 | 0.625 | 0.815 | 0.833 | 0.450 | 0.750 |
| direct_fim | nova-2-lite | 20 | 0.590 | 0.625 | 0.785 | 0.833 | 0.125 | 0.800 |
| direct_fim | nova-pro | 20 | 0.597 | 0.614 | 0.798 | 0.793 | 0.250 | 0.750 |
| direct_fim | qwen3-coder-flash | 20 | 0.603 | 0.616 | 0.808 | 0.821 | 0.318 | 0.750 |
| direct_fim | qwen3.6-plus | 20 | 0.625 | 0.658 | 0.835 | 0.896 | 0.350 | 0.750 |
| direct_reference_open | deepseek-v3.2 | 20 | 0.540 | 0.576 | 0.668 | 0.712 | 0.180 | 0.783 |
| direct_reference_open | gemini-2.5-flash | 20 | 0.629 | 0.630 | 0.777 | 0.789 | 0.360 | 0.833 |
| direct_reference_open | gemini-2.5-pro | 20 | 0.625 | 0.692 | 0.772 | 0.843 | 0.325 | 0.780 |
| direct_reference_open | gpt-5.4 | 20 | 0.642 | 0.680 | 0.792 | 0.850 | 0.260 | 0.814 |
| direct_reference_open | gpt-5.4-mini | 20 | 0.644 | 0.640 | 0.795 | 0.800 | 0.340 | 0.857 |
| direct_reference_open | granite-4.0-h-small | 20 | 0.586 | 0.572 | 0.726 | 0.701 | 0.420 | 0.725 |
| direct_reference_open | granite-4.0-h-tiny-local | 20 | 0.453 | 0.357 | 0.557 | 0.437 | 0.200 | 0.800 |
| direct_reference_open | grok-4-1-fast-reasoning | 20 | 0.678 | 0.728 | 0.838 | 0.890 | 0.420 | 0.843 |
| direct_reference_open | mistral-large-3 | 20 | 0.674 | 0.700 | 0.833 | 0.850 | 0.420 | 0.814 |
| direct_reference_open | nova-2-lite | 20 | 0.632 | 0.663 | 0.782 | 0.812 | 0.433 | 0.800 |
| direct_reference_open | nova-pro | 20 | 0.611 | 0.628 | 0.754 | 0.781 | 0.425 | 0.843 |
| direct_reference_open | qwen3-coder-flash | 20 | 0.645 | 0.670 | 0.799 | 0.837 | 0.233 | 0.780 |
| direct_reference_open | qwen3.6-plus | 20 | 0.647 | 0.617 | 0.799 | 0.755 | 0.440 | 0.817 |
| agentic_free | deepseek-v3.2 | 20 | 0.593 | 0.653 | 0.804 | 0.912 | 0.159 | 0.800 |
| agentic_free | gemini-2.5-flash | 20 | 0.665 | 0.686 | 0.899 | 1.000 | 0.300 | 0.800 |
| agentic_free | gemini-2.5-pro | 20 | 0.618 | 0.650 | 0.832 | 0.867 | 0.206 | 0.800 |
| agentic_free | gpt-5.4 | 20 | 0.614 | 0.628 | 0.834 | 0.833 | 0.316 | 0.800 |
| agentic_free | gpt-5.4-mini | 20 | 0.618 | 0.658 | 0.839 | 1.000 | 0.267 | 0.800 |
| agentic_free | granite-4.0-h-small | 20 | 0.559 | 0.548 | 0.753 | 0.767 | 0.133 | 0.800 |
| agentic_free | grok-4-1-fast-reasoning | 20 | 0.577 | 0.630 | 0.781 | 0.871 | 0.000 | 0.800 |
| agentic_free | mistral-large-3 | 20 | 0.660 | 0.667 | 0.892 | 0.894 | 0.300 | 0.800 |
| agentic_free | nova-pro | 20 | 0.658 | 0.667 | 0.897 | 1.000 | 0.500 | 0.800 |
| agentic_free | qwen3.6-plus | 20 | 0.627 | 0.667 | 0.851 | 0.883 | 0.133 | 0.800 |
| agentic_informed | deepseek-v3.2 | 20 | 0.692 | 0.724 | 0.860 | 0.887 | 0.350 | 0.833 |
| agentic_informed | gemini-2.5-flash | 20 | 0.700 | 0.721 | 0.869 | 0.900 | 0.400 | 0.833 |
| agentic_informed | gemini-2.5-pro | 20 | 0.726 | 0.720 | 0.903 | 0.900 | 0.533 | 0.833 |
| agentic_informed | gpt-5.4 | 20 | 0.719 | 0.720 | 0.896 | 0.900 | 0.560 | 0.833 |
| agentic_informed | gpt-5.4-mini | 20 | 0.690 | 0.678 | 0.859 | 0.867 | 0.433 | 0.833 |
| agentic_informed | granite-4.0-h-small | 20 | 0.451 | 0.460 | 0.563 | 0.563 | 0.150 | 0.771 |
| agentic_informed | grok-4-1-fast-reasoning | 20 | 0.667 | 0.735 | 0.833 | 0.923 | 0.333 | 0.833 |
| agentic_informed | mistral-large-3 | 20 | 0.465 | 0.472 | 0.578 | 0.567 | 0.000 | 0.833 |
| agentic_informed | nova-pro | 20 | 0.385 | 0.397 | 0.486 | 0.493 | 0.167 | 0.667 |
| agentic_informed | qwen3.6-plus | 20 | 0.739 | 0.772 | 0.921 | 1.000 | 0.433 | 0.833 |
