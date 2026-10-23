# Provider Gini Index

Run: `direct/complete/full_5c`; modality: `nli`; level: `provider`; counting: `occurrence`.
The provider universe is the scenario-wide union across all models, matching arXiv:2501.07849.

For a scenario with `n` providers, raw GI ranges from `0` to `(n-1)/n`; normalized GI divides by that attainable maximum.

| Model | Scenarios | Mean GI | Median GI | Mean normalized GI | Median normalized GI | Min | Max |
|---|---:|---:|---:|---:|---:|---:|---:|
| deepseek-v3.2 | 20 | 0.646 | 0.667 | 0.812 | 0.847 | 0.267 | 0.875 |
| gemini-2.5-flash | 20 | 0.663 | 0.688 | 0.834 | 0.883 | 0.333 | 0.864 |
| gemini-2.5-pro | 20 | 0.613 | 0.614 | 0.774 | 0.805 | 0.367 | 0.825 |
| gpt-5.4 | 20 | 0.643 | 0.671 | 0.813 | 0.854 | 0.275 | 0.875 |
| gpt-5.4-mini | 20 | 0.602 | 0.581 | 0.757 | 0.700 | 0.233 | 0.857 |
| granite-4.0-h-small | 20 | 0.614 | 0.600 | 0.776 | 0.744 | 0.400 | 0.833 |
| granite-4.0-h-tiny-local | 18 | 0.664 | 0.708 | 0.847 | 0.897 | 0.167 | 0.875 |
| grok-4-1-fast-reasoning | 20 | 0.682 | 0.673 | 0.865 | 0.877 | 0.425 | 0.833 |
| mistral-large-3 | 20 | 0.683 | 0.680 | 0.862 | 0.852 | 0.400 | 0.889 |
| nova-2-lite | 20 | 0.684 | 0.707 | 0.863 | 0.910 | 0.278 | 0.875 |
| nova-pro | 20 | 0.549 | 0.525 | 0.687 | 0.693 | 0.250 | 0.812 |
| qwen3-coder-flash | 20 | 0.695 | 0.742 | 0.880 | 0.925 | 0.367 | 0.875 |
| qwen3.6-plus | 20 | 0.687 | 0.700 | 0.873 | 0.867 | 0.480 | 0.850 |
