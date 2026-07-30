# Benchmark Catalogs

This directory contains the benchmark data, prompts, model registries, and evidence bundles used by VIBench.

## Families

- [`vibench`](vibench): current benchmark, published at `vibench-emnlp26/vibench`
- Published benchmark dataset: `vibench-emnlp26/vibench`

## Current Benchmark Layout

```text
benchmark/vibench/
├── README.md
├── models.json
├── system_prompt.txt
├── agentic_system_prompt.txt
├── scenario_id_map.json
├── direct/
│   └── tasks.jsonl
├── agentic/
│   └── tasks.jsonl
├── evidence/
│   ├── provider_tools_and_proofs.json
│   ├── provider_urls.txt
│   ├── notes/
│   ├── registry/
│   │   ├── proofs.jsonl
│   │   └── scenario_proofs.jsonl
│   ├── generated/
│   │   ├── provider_card_line_audit.json
│   │   ├── provider_url_check.tsv
│   │   ├── provider_doc_snapshots.json
│   │   ├── provider_doc_snapshots_summary.json
│   │   ├── provider_doc_snapshot_quality.json
│   │   ├── provider_doc_snapshot_quality_summary.json
│   │   ├── provider_doc_snapshot_quality_report.md
│   │   ├── alignment_check_summary.json
│   │   └── alignment_check_report.md
│   └── snapshots/
└── vibench.jsonl
```

## Active Benchmark

`vibench`

- current paper-facing benchmark
- 20 direct scenarios
- 20 agentic workflows
- current agentic runners default directly to the agentic workflow catalog
- HuggingFace-style task rows plus proof metadata
- current benchmark findings are summarized in
  `../docs/results/current_results.md`

For new work, use `benchmark/vibench/`.
