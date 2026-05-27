# Results

This directory mirrors the active study layout and keeps lightweight
paper-facing pointers. The raw and labeled artifacts remain in `outputs/runs/`;
the narrative reports remain in `docs/results/`.

```text
results/
├── direct/
│   ├── complete/
│   └── ablations/option_order/
└── agentic/
    ├── complete/
    └── ablations/option_order/
```

Published result bundles should be synchronized through:

`https://huggingface.co/datasets/vibench-emnlp26/vibench-results`

Current retained result inventory:

- 24,698 indexed labeled records across complete runs and ablations.
- 15,600 main direct generations.
- 2,000 main OpenCode agentic sessions.
- 1,818 Agents SDK robustness sessions.
- 5,280 option-order/omission ablation records.
- 76,786 retained raw generation files.

The explorer can read this dataset directly:

```bash
cd ../..
HF_TOKEN=... python explorer/server.py \
  --benchmark-source hf \
  --results-source hf \
  --hf-benchmark-repo vibench-emnlp26/vibench \
  --hf-results-repo vibench-emnlp26/vibench-results
```

Regenerate the paper/explorer charts from the retained results with:

```bash
make figures
```
