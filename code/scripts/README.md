# Scripts

Scripts are grouped by function:

- [`scripts/generation`](generation): run direct and agentic generations
- [`scripts/evaluation`](evaluation): detection, scoring, report generation, audits
- [`scripts/plotting`](plotting): figure rendering
- [`scripts/benchmark`](benchmark): benchmark construction and validation utilities
- [`scripts/utils`](utils): smaller operational helpers

Two utilities sit at this level: [`scripts/browse.py`](browse.py), which reads the
benchmark and the generated outputs in the terminal (`make scenarios`, `make models`,
`make runs`, `make browse ARGS=...`), and the dataset loader
[`scripts/vibench_loader.py`](vibench_loader.py).
