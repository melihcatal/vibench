---
license: mit
pretty_name: VIBench
task_categories:
  - text-generation
language:
  - en
tags:
  - code-generation
  - software-engineering
  - benchmark
  - llm-evaluation
  - vertical-integration-bias
  - agentic
size_categories:
  - n<1K
configs:
  - config_name: direct
    data_files:
      - split: tasks
        path: direct/tasks.jsonl
  - config_name: agentic
    data_files:
      - split: tasks
        path: agentic/tasks.jsonl
---

# VIBench

Local source-of-truth benchmark corpus for measuring **Vertical-Integration
Bias (VIB)** in LLM code generation. The nested task definitions live here in
`direct/tasks.jsonl` and `agentic/tasks.jsonl`. The published Hugging Face
dataset at [sealifi/vibench](https://huggingface.co/datasets/sealifi/vibench)
ships flattened viewer tables derived from these files, plus the evidence,
audit, and validation bundles.

## Current empirical snapshot

The current retained results show a stable but non-universal VIB pattern:

- direct affiliated preference is strongest for `gemini-2.5-flash`,
  `nova-pro`, and `gpt-5.4-mini`;
- agentic generation strengthens those effects in both the OpenCode and
  Agents SDK runtimes;
- the strongest current lock-in / leakage signals are again led by
  `gemini-2.5-flash` and `nova-pro`;
- `gpt-5.4-mini` remains clearly positive, while `gpt-5.4` is weaker and less
  stable than the top models;
- IBM models remain weak on direct self-preference, with Granite showing more
  downstream leakage than raw affiliated selection.

Use `docs/results/current_results.md (generated; see code/benchmark/README.md)` for the exact current tables.

## Benchmark task files

| File | Rows | What it is |
|---|---:|---|
| `direct/tasks.jsonl` | 20 | One row per direct scenario, with provider/neutral tool cards, nested subtasks, and coverage labels. |
| `agentic/tasks.jsonl` | 20 | One row per multi-file workflow aligned to a direct scenario. |

The HF viewer uses flattened exports rather than these nested rows:

| HF viewer config | Source in published dataset | Rows |
|---|---|---:|
| `direct` | `viewer/direct.jsonl` | 80 |
| `agentic` | `viewer/agentic.jsonl` | 20 |

So:

- use the HF `direct` / `agentic` configs when you want the flattened viewer
  tables;
- use the local repo files or downloadable root artifacts when you want the
  nested source-of-truth rows.

Example for the downloadable nested rows:

```python
from huggingface_hub import hf_hub_download

direct_path = hf_hub_download("sealifi/vibench", "tasks_direct.jsonl", repo_type="dataset")
agentic_path = hf_hub_download("sealifi/vibench", "tasks_agentic.jsonl", repo_type="dataset")
```

## Downloadable-only files (not in the viewer)

These ship with the repository and are part of the reproducibility package,
but are **not** exposed as HF configs because their schemas are either
heterogeneous (different fields per row) or have open-ended struct children
that clash with the viewer's Arrow type inference.

| File | Why it's not a config | How to load |
|---|---|---|
| `vibench.jsonl` | Union of direct + agentic rows with an added `stage` field — 2 distinct schemas in one file | `huggingface_hub.hf_hub_download(repo_id="sealifi/vibench", filename="vibench.jsonl", repo_type="dataset")` |
| `audit/vibench_detector_audit.jsonl` | Mixed direct/agentic samples with a `sibling_files` dict that has ~170 open-ended filename keys | Same `hf_hub_download` pattern |
| `evidence/provider_tools_and_proofs.json` | Single nested benchmark-wide object, not a row-shaped dataset | `hf_hub_download` |
| `evidence/generated/alignment_check_summary.json` | Single object | `hf_hub_download` |
| `evidence/generated/alignment_check_report.md` | Markdown, not tabular | `hf_hub_download` |
| `evidence/generated/provider_url_check.tsv` | TSV with reachability status per URL | `hf_hub_download` |
| `evidence/generated/provider_url_check_summary.json` | Single object (HTTP-status counts) | `hf_hub_download` |
| `evidence/provider_urls.txt` | Flat URL list | `hf_hub_download` |
| `evidence/registry/proofs.jsonl` | One row per unique cited proof page with stable `proof_id` | `hf_hub_download` |
| `evidence/registry/scenario_proofs.jsonl` | Scenario-to-proof mapping rows keyed by `proof_id` | `hf_hub_download` |
| `evidence/generated/provider_doc_snapshots.json` | Snapshot manifest for all cited URLs | `hf_hub_download` |
| `evidence/generated/provider_doc_snapshots_summary.json` | Snapshot status/count summary | `hf_hub_download` |
| `evidence/generated/provider_doc_snapshot_quality.json` | Per-URL snapshot quality audit | `hf_hub_download` |
| `evidence/generated/provider_doc_snapshot_quality_summary.json` | Snapshot quality counts and flagged URLs | `hf_hub_download` |
| `evidence/generated/provider_doc_snapshot_quality_report.md` | Human-readable snapshot quality report | `hf_hub_download` |
| `evidence/notes/` | Freeform methodology notes and scenario-design memos | `hf_hub_download` |
| `evidence/snapshots/` | Archived response bodies for cited official-doc URLs | `hf_hub_download` |
| `system_prompt.txt`, `agentic_system_prompt.txt` | Plain text prompt sources | `hf_hub_download` |
| `models.json`, `scenario_id_map.json` | Metadata objects | `hf_hub_download` |

## Unloaded evidence files

These are repository assets that the dataset viewer does not load as a
split because they are not in a row-based format, but they ship with the
dataset and are part of the reproducibility package:

| File | Shape | What it proves |
|---|---|---|
| `evidence/provider_tools_and_proofs.json` | nested JSON (benchmark-wide) | Documented provider tools per scenario with SDK/REST/protocol markers and supplemental cards |
| `evidence/generated/alignment_check_summary.json` | JSON object | Direct/agentic scenario counts, label counts, consistency checks |
| `evidence/generated/alignment_check_report.md` | Markdown | Human-readable alignment report across the benchmark |
| `evidence/generated/provider_url_check.tsv` | TSV | Reachability check for every provider doc URL cited |
| `evidence/generated/provider_url_check_summary.json` | JSON object | HTTP status counts for the URL check |
| `evidence/provider_urls.txt` | Text | Flat list of all cited provider doc URLs |
| `evidence/registry/proofs.jsonl` | JSONL | Stable proof registry keyed by `proof_id` with URL, title, domain, and scenario usage |
| `evidence/registry/scenario_proofs.jsonl` | JSONL | Scenario-level mapping from provider/neutral tool cards to stable `proof_id`s |
| `evidence/generated/provider_doc_snapshots.json` | JSON array | One archival snapshot record per cited provider-doc URL |
| `evidence/generated/provider_doc_snapshots_summary.json` | JSON object | Snapshot capture counts and status totals |
| `evidence/generated/provider_doc_snapshot_quality.json` | JSON array | Quality label, flags, title/H1 extraction, and text excerpt for each archived provider-doc snapshot |
| `evidence/generated/provider_doc_snapshot_quality_summary.json` | JSON object | Quality-count summary and flagged weak/review snapshot URLs |
| `evidence/generated/provider_doc_snapshot_quality_report.md` | Markdown | Human-readable review list for weak or ambiguous snapshot captures |
| `evidence/notes/` | directory | Freeform methodology notes and scenario-design memos retained with the artifact bundle |
| `evidence/snapshots/` | directory | Saved response bodies for cited provider-doc URLs |
| `system_prompt.txt` | Text | Exact direct-generation system prompt |
| `agentic_system_prompt.txt` | Text | Exact agentic-generation system prompt |
| `models.json` | JSON | Model roster with affiliation and provider-family metadata |
| `scenario_id_map.json` | JSON | Mapping between legacy and current scenario IDs |

The evidence bundle in `evidence/` and `evidence/snapshots/` backs the
benchmark's provider-selection decisions: every documented provider option has
a real SDK/REST/protocol surface, a cited official-doc URL tracked in the
reachability artifacts, a local archival snapshot, and a matched reference
card.

The live reachability check and the local snapshot archive are intentionally
separate. Some vendor doc sites return different statuses to different clients;
the snapshot archive preserves the fetched content used for the benchmark even
when a later live probe disagrees. The snapshot-quality audit then checks that
those saved `200` responses still look like real page content rather than a
generic shell or access/error page.

The current benchmark definition also includes an `Observability` family:

- `S19`: `Managed Metrics Monitoring`
- `S20`: `Managed Log Query / Log Ingestion`

These rows are part of the benchmark and evidence bundle now. Existing
paper-facing result tables may still reflect runs collected before the
observability rows were added.

## Direct Dataset

- File: `direct/tasks.jsonl`
- Format: HuggingFace-style JSONL, one scenario per row.
- Scenarios: 20
- Subtasks per scenario: 4
- One default dataset with AWS, Google, Microsoft/OpenAI/Azure, Alibaba, IBM where eligible, and neutral controls.
- IBM: included when eligible; `coverage.all5` marks rows valid for All-5 affiliated analysis.

## Agentic Dataset

- File: `agentic/tasks.jsonl`
- Format: HuggingFace-style JSONL, one workflow per row.
- Each workflow has 10 expected files:
  - 4 aligned core files mapped to direct subtasks
  - 2 local context files
  - 4 downstream extension files
- Scored files per workflow: 8
- Downstream scored files are labeled with `coupling_expectation`:
  - `independent_expected` for strong cross-domain cascade probes
  - `compatible_but_independent` for related follow-up steps

## Important Columns

- `provider_tools`: documented provider options with SDK/REST/protocol markers.
- `official_docs`: source URLs used as evidence.
- `official_docs[].proof_id`: stable proof identifier derived from the cited URL.
- `provider_proof_ids`, `neutral_proof_ids`, `proof_ids`: row-level flattened proof-id lists for direct and agentic tasks.
- `coverage`: Core-4 and All-5 eligibility metadata.
- `notes`: caveats about asymmetry, REST use, or taxonomy differences.
- `components`: agentic file mapping to direct subtasks and cascade roles.

## Prompt-Balance Notes

- Direct open-reference (`reference_open`) prompts use a deterministic
  scenario-specific base order and rotate it per completion. The listed
  providers are known suitable references, not a closed menu; models may use
  another concrete identifiable provider.
- Agentic informed prompts use the same deterministic scenario-specific base
  order and per-completion rotation for matching scenario blocks.
- Agentic prompts use neutral file-group labels for same-scenario files, local
  helper files, and later-step files. The prompt does not instruct models to
  reuse one provider across files.
- Direct provider cards use the same model-facing line template across providers:
  label, service, SDK, interface, operations, setup hints, and official docs.
- Agentic informed prompts use a shorter one-line provider summary per option:
  label plus service, SDK, interface, and auth hints.
- Metadata notes remain in the dataset for human documentation but are not shown
  in model-facing prompts. Proof URLs are shown in direct `reference_open`
  provider cards and retained in evidence metadata.
- `evidence/generated/provider_card_line_audit.json` records line counts, character
  counts, and approximate token counts for every rendered direct provider card.
- Equal line count is enforced by construction. Character and token counts can
  still vary because provider names, URLs, SDK names, and operation names differ.
  Those residual differences should be reported as a formatting caveat rather
  than silently ignored.

## Combined Artifact

- File: `vibench.jsonl`
- Contains both stages with a `stage` column:
  - `direct`
  - `agentic`

## Sampling

- Canonical VIBench configs use provider-default sampling.
- `temperature`, `max_tokens`, and `top_p` are inherited as `null` from `configs/default.yaml` unless a run config or CLI flag overrides them.
- Direct mode therefore omits those parameters from LiteLLM calls by default.
- The controlled agentic runner uses OpenAI Agents SDK + LiteLLM and likewise omits those parameters by default. The OpenCode agentic config is kept as a robustness runner.
