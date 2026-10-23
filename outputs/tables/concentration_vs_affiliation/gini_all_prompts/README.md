# Gini Index Across Prompt Settings

Paper-style scenario-wide provider universes are computed independently within each setting.
Agentic results use `aligned_core` components; multi-label counting is `occurrence`.
Agentic `free` corresponds to NLI-style prompting and `informed` to Reference-Open-style prompting; there is no agentic FIM condition.

## Setting-Level Results

Raw GI has scenario-specific maximum `(n-1)/n`; normalized GI divides by this maximum and ranges from 0 to 1.

| Setting | Valid / total | Mean GI | Median GI | Mean normalized | Median normalized | Min | Max |
|---|---:|---:|---:|---:|---:|---:|---:|
| direct_nli | 258 / 260 | 0.648 | 0.667 | 0.818 | 0.843 | 0.167 | 0.889 |
| direct_fim | 258 / 260 | 0.638 | 0.667 | 0.822 | 0.854 | 0.075 | 0.889 |
| direct_reference_open | 260 / 260 | 0.625 | 0.650 | 0.766 | 0.800 | 0.200 | 0.857 |
| agentic_free | 200 / 200 | 0.650 | 0.677 | 0.851 | 0.908 | 0.000 | 0.857 |
| agentic_informed | 200 / 200 | 0.632 | 0.669 | 0.782 | 0.858 | 0.000 | 0.875 |

## Model-Level Results

| Setting | Model | Scenarios | Mean GI | Median GI | Mean normalized | Median normalized | Min | Max |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| direct_nli | deepseek-v3.2 | 20 | 0.646 | 0.667 | 0.812 | 0.847 | 0.267 | 0.875 |
| direct_nli | gemini-2.5-flash | 20 | 0.663 | 0.688 | 0.834 | 0.883 | 0.333 | 0.864 |
| direct_nli | gemini-2.5-pro | 20 | 0.613 | 0.614 | 0.774 | 0.805 | 0.367 | 0.825 |
| direct_nli | gpt-5.4 | 20 | 0.643 | 0.671 | 0.813 | 0.854 | 0.275 | 0.875 |
| direct_nli | gpt-5.4-mini | 20 | 0.602 | 0.581 | 0.757 | 0.700 | 0.233 | 0.857 |
| direct_nli | granite-4.0-h-small | 20 | 0.614 | 0.600 | 0.776 | 0.744 | 0.400 | 0.833 |
| direct_nli | granite-4.0-h-tiny-local | 18 | 0.664 | 0.708 | 0.847 | 0.897 | 0.167 | 0.875 |
| direct_nli | grok-4-1-fast-reasoning | 20 | 0.682 | 0.673 | 0.865 | 0.877 | 0.425 | 0.833 |
| direct_nli | mistral-large-3 | 20 | 0.683 | 0.680 | 0.862 | 0.852 | 0.400 | 0.889 |
| direct_nli | nova-2-lite | 20 | 0.684 | 0.707 | 0.863 | 0.910 | 0.278 | 0.875 |
| direct_nli | nova-pro | 20 | 0.549 | 0.525 | 0.687 | 0.693 | 0.250 | 0.812 |
| direct_nli | qwen3-coder-flash | 20 | 0.695 | 0.742 | 0.880 | 0.925 | 0.367 | 0.875 |
| direct_nli | qwen3.6-plus | 20 | 0.687 | 0.700 | 0.873 | 0.867 | 0.480 | 0.850 |
| direct_fim | deepseek-v3.2 | 20 | 0.698 | 0.700 | 0.902 | 0.912 | 0.500 | 0.833 |
| direct_fim | gemini-2.5-flash | 20 | 0.635 | 0.646 | 0.818 | 0.831 | 0.375 | 0.889 |
| direct_fim | gemini-2.5-pro | 20 | 0.589 | 0.590 | 0.753 | 0.775 | 0.275 | 0.838 |
| direct_fim | gpt-5.4 | 20 | 0.595 | 0.637 | 0.766 | 0.805 | 0.075 | 0.750 |
| direct_fim | gpt-5.4-mini | 20 | 0.589 | 0.613 | 0.759 | 0.805 | 0.360 | 0.780 |
| direct_fim | granite-4.0-h-small | 20 | 0.577 | 0.593 | 0.746 | 0.791 | 0.304 | 0.816 |
| direct_fim | granite-4.0-h-tiny-local | 18 | 0.735 | 0.750 | 0.944 | 1.000 | 0.500 | 0.889 |
| direct_fim | grok-4-1-fast-reasoning | 20 | 0.646 | 0.678 | 0.831 | 0.900 | 0.400 | 0.825 |
| direct_fim | mistral-large-3 | 20 | 0.662 | 0.667 | 0.855 | 0.861 | 0.500 | 0.767 |
| direct_fim | nova-2-lite | 20 | 0.626 | 0.685 | 0.800 | 0.850 | 0.125 | 0.875 |
| direct_fim | nova-pro | 20 | 0.645 | 0.684 | 0.833 | 0.851 | 0.400 | 0.780 |
| direct_fim | qwen3-coder-flash | 20 | 0.645 | 0.667 | 0.833 | 0.833 | 0.318 | 0.833 |
| direct_fim | qwen3.6-plus | 20 | 0.666 | 0.710 | 0.858 | 0.917 | 0.375 | 0.817 |
| direct_reference_open | deepseek-v3.2 | 20 | 0.555 | 0.576 | 0.680 | 0.708 | 0.317 | 0.783 |
| direct_reference_open | gemini-2.5-flash | 20 | 0.639 | 0.647 | 0.783 | 0.789 | 0.360 | 0.833 |
| direct_reference_open | gemini-2.5-pro | 20 | 0.635 | 0.692 | 0.777 | 0.843 | 0.325 | 0.817 |
| direct_reference_open | gpt-5.4 | 20 | 0.649 | 0.680 | 0.793 | 0.850 | 0.260 | 0.817 |
| direct_reference_open | gpt-5.4-mini | 20 | 0.649 | 0.645 | 0.794 | 0.800 | 0.340 | 0.857 |
| direct_reference_open | granite-4.0-h-small | 20 | 0.597 | 0.576 | 0.734 | 0.698 | 0.420 | 0.767 |
| direct_reference_open | granite-4.0-h-tiny-local | 20 | 0.468 | 0.400 | 0.571 | 0.500 | 0.200 | 0.800 |
| direct_reference_open | grok-4-1-fast-reasoning | 20 | 0.682 | 0.698 | 0.836 | 0.855 | 0.420 | 0.844 |
| direct_reference_open | mistral-large-3 | 20 | 0.681 | 0.692 | 0.834 | 0.862 | 0.420 | 0.833 |
| direct_reference_open | nova-2-lite | 20 | 0.641 | 0.663 | 0.787 | 0.812 | 0.440 | 0.800 |
| direct_reference_open | nova-pro | 20 | 0.620 | 0.650 | 0.758 | 0.800 | 0.425 | 0.843 |
| direct_reference_open | qwen3-coder-flash | 20 | 0.655 | 0.670 | 0.806 | 0.837 | 0.343 | 0.800 |
| direct_reference_open | qwen3.6-plus | 20 | 0.654 | 0.638 | 0.801 | 0.755 | 0.440 | 0.843 |
| agentic_free | deepseek-v3.2 | 20 | 0.620 | 0.667 | 0.816 | 0.910 | 0.155 | 0.833 |
| agentic_free | gemini-2.5-flash | 20 | 0.695 | 0.750 | 0.903 | 1.000 | 0.300 | 0.857 |
| agentic_free | gemini-2.5-pro | 20 | 0.655 | 0.710 | 0.851 | 0.893 | 0.206 | 0.833 |
| agentic_free | gpt-5.4 | 20 | 0.641 | 0.658 | 0.843 | 0.867 | 0.316 | 0.833 |
| agentic_free | gpt-5.4-mini | 20 | 0.647 | 0.702 | 0.847 | 0.920 | 0.267 | 0.857 |
| agentic_free | granite-4.0-h-small | 20 | 0.585 | 0.621 | 0.763 | 0.778 | 0.250 | 0.857 |
| agentic_free | grok-4-1-fast-reasoning | 20 | 0.613 | 0.673 | 0.803 | 0.880 | 0.000 | 0.833 |
| agentic_free | mistral-large-3 | 20 | 0.693 | 0.667 | 0.903 | 0.925 | 0.300 | 0.833 |
| agentic_free | nova-pro | 20 | 0.687 | 0.706 | 0.904 | 1.000 | 0.500 | 0.857 |
| agentic_free | qwen3.6-plus | 20 | 0.664 | 0.721 | 0.875 | 0.900 | 0.350 | 0.814 |
| agentic_informed | deepseek-v3.2 | 20 | 0.697 | 0.737 | 0.860 | 0.897 | 0.350 | 0.833 |
| agentic_informed | gemini-2.5-flash | 20 | 0.712 | 0.735 | 0.877 | 0.900 | 0.400 | 0.857 |
| agentic_informed | gemini-2.5-pro | 20 | 0.736 | 0.728 | 0.908 | 0.900 | 0.533 | 0.857 |
| agentic_informed | gpt-5.4 | 20 | 0.721 | 0.718 | 0.891 | 0.900 | 0.560 | 0.875 |
| agentic_informed | gpt-5.4-mini | 20 | 0.693 | 0.650 | 0.857 | 0.867 | 0.514 | 0.833 |
| agentic_informed | granite-4.0-h-small | 20 | 0.472 | 0.474 | 0.584 | 0.563 | 0.217 | 0.771 |
| agentic_informed | grok-4-1-fast-reasoning | 20 | 0.669 | 0.735 | 0.830 | 0.929 | 0.358 | 0.833 |
| agentic_informed | mistral-large-3 | 20 | 0.475 | 0.489 | 0.587 | 0.624 | 0.000 | 0.833 |
| agentic_informed | nova-pro | 20 | 0.400 | 0.463 | 0.501 | 0.571 | 0.143 | 0.667 |
| agentic_informed | qwen3.6-plus | 20 | 0.748 | 0.772 | 0.926 | 1.000 | 0.514 | 0.857 |
