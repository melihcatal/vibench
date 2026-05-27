#!/usr/bin/env python3
"""Prepare private Hugging Face dataset upload folders for VIBench."""

from __future__ import annotations

import argparse
import json
import shutil
import textwrap
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PACKAGE_ROOT = ROOT.parent
BENCHMARK = ROOT / "benchmark" / "vibench"
OUTPUTS = ROOT / "outputs" / "runs"
RESULTS = ROOT / "results"
DOC_RESULTS = ROOT / "docs" / "results"
DOC_FIGURES = ROOT / "docs" / "figures"
CONFIGS = ROOT / "configs" / "vibench"
PACKAGE_FIGURES = PACKAGE_ROOT / "figures"
VALIDATION = ROOT / "validation"


def copy_file(src: Path, dst: Path) -> None:
    if not src.exists():
        raise FileNotFoundError(src)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def copy_dir(src: Path, dst: Path) -> None:
    if not src.exists():
        raise FileNotFoundError(src)
    if dst.exists():
        shutil.rmtree(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dst)


def copy_optional_dir(src: Path, dst: Path) -> None:
    if src.exists():
        copy_dir(src, dst)


def count_files(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for p in path.rglob("*") if p.is_file())


def count_jsonl_rows(path: Path) -> int:
    if not path.exists():
        return 0
    with open(path) as handle:
        return sum(1 for line in handle if line.strip())


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(text).strip() + "\n", encoding="utf-8")


def classify_run_category(run_id: str) -> str:
    if run_id.startswith("direct/complete/"):
        return "direct_complete"
    if run_id.startswith("direct/ablations/"):
        return "direct_ablations"
    if run_id.startswith("agentic/complete/opencode"):
        return "opencode_complete"
    if run_id.startswith("agentic/complete/agents_sdk"):
        return "agents_sdk_complete"
    if run_id.startswith("agentic/ablations/option_order/opencode"):
        return "opencode_ablations"
    if run_id.startswith("agentic/ablations/option_order/agents_sdk"):
        return "agents_sdk_ablations"
    return "other"


def public_prompt_variant(modality: str, variant: str = "") -> str:
    if modality == "agentic":
        return {"free": "nli", "informed": "ref", "nli": "nli", "ref": "ref"}.get(variant, "nli")
    return {"nli": "nli", "fim": "fim", "reference_open": "ref", "ref": "ref"}.get(modality, modality)


def _flatten_tool_values(tools: list[dict], field: str) -> str:
    values = []
    seen = set()
    for tool in tools:
        value = str(tool.get(field, "")).strip()
        if value and value not in seen:
            seen.add(value)
            values.append(value)
    return " | ".join(values)


def _flatten_tool_docs(tools: list[dict]) -> tuple[str, str]:
    titles = []
    urls = []
    seen_titles = set()
    seen_urls = set()
    for tool in tools:
        for doc in tool.get("official_docs") or []:
            title = str(doc.get("title", "")).strip()
            url = str(doc.get("url", "")).strip()
            if title and title not in seen_titles:
                seen_titles.add(title)
                titles.append(title)
            if url and url not in seen_urls:
                seen_urls.add(url)
                urls.append(url)
    return " | ".join(titles), " | ".join(urls)


def _flatten_tool_doc_ids(tools: list[dict]) -> str:
    proof_ids = []
    seen = set()
    for tool in tools:
        for doc in tool.get("official_docs") or []:
            proof_id = str(doc.get("proof_id", "")).strip()
            if proof_id and proof_id not in seen:
                seen.add(proof_id)
                proof_ids.append(proof_id)
    return " | ".join(proof_ids)


def _eligible_provider_keys(coverage: dict) -> str:
    return ",".join(
        provider_key
        for provider_key, info in sorted((coverage.get("providers") or {}).items())
        if info.get("eligible")
    )


def build_benchmark_viewer_tables(out_dir: Path) -> None:
    direct_rows = [
        json.loads(line)
        for line in (BENCHMARK / "direct" / "tasks.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    agentic_rows = [
        json.loads(line)
        for line in (BENCHMARK / "agentic" / "tasks.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    direct_task_rows = []
    agentic_task_rows = []
    direct_by_scenario = {row.get("scenario_id", ""): row for row in direct_rows}

    for row in direct_rows:
        scenario_id = row.get("scenario_id", "")
        coverage = row.get("coverage") or {}
        provider_tools = row.get("provider_tools") or []
        neutral_tools = row.get("neutral_tools") or []
        provider_doc_titles, provider_doc_urls = _flatten_tool_docs(provider_tools)
        neutral_doc_titles, neutral_doc_urls = _flatten_tool_docs(neutral_tools)
        provider_doc_ids = _flatten_tool_doc_ids(provider_tools)
        neutral_doc_ids = _flatten_tool_doc_ids(neutral_tools)

        for subtask in row.get("subtasks") or []:
            direct_task_rows.append({
                "scenario_id": scenario_id,
                "title": row.get("title", ""),
                "family": row.get("family", ""),
                "competition": row.get("competition", ""),
                "notes": row.get("notes", ""),
                "core4": bool(coverage.get("core4")),
                "all5": bool(coverage.get("all5")),
                "eligible_providers": _eligible_provider_keys(coverage),
                "subtask_id": subtask.get("subtask_id", ""),
                "index": subtask.get("index"),
                "role": subtask.get("role", ""),
                "file": subtask.get("file", ""),
                "description": subtask.get("description", ""),
                "nli_task_id": (subtask.get("direct_task_ids") or {}).get("nli", ""),
                "fim_task_id": (subtask.get("direct_task_ids") or {}).get("fim", ""),
                "reference_open_task_id": (subtask.get("direct_task_ids") or {}).get("reference_open", ""),
                "nli_prompt": subtask.get("nli_prompt", ""),
                "reference_open_task_prompt": subtask.get("reference_open_task_prompt", ""),
                "provider_services": _flatten_tool_values(provider_tools, "service"),
                "provider_sdks": _flatten_tool_values(provider_tools, "sdk"),
                "provider_interfaces": _flatten_tool_values(provider_tools, "interface"),
                "provider_operations": " | ".join(
                    ", ".join(tool.get("operations") or []) for tool in provider_tools if tool.get("operations")
                ),
                "provider_proof_titles": provider_doc_titles,
                "provider_proof_urls": provider_doc_urls,
                "provider_proof_ids": provider_doc_ids,
                "neutral_services": _flatten_tool_values(neutral_tools, "service"),
                "neutral_sdks": _flatten_tool_values(neutral_tools, "sdk"),
                "neutral_interfaces": _flatten_tool_values(neutral_tools, "interface"),
                "neutral_operations": " | ".join(
                    ", ".join(tool.get("operations") or []) for tool in neutral_tools if tool.get("operations")
                ),
                "neutral_proof_titles": neutral_doc_titles,
                "neutral_proof_urls": neutral_doc_urls,
                "neutral_proof_ids": neutral_doc_ids,
                "proof_ids": " | ".join(part for part in [provider_doc_ids, neutral_doc_ids] if part),
            })

    for row in agentic_rows:
        scenario_id = row.get("primary_atomic_scenario", "")
        direct_row = direct_by_scenario.get(scenario_id, {})
        coverage = direct_row.get("coverage") or {}
        provider_tools = direct_row.get("provider_tools") or []
        neutral_tools = direct_row.get("neutral_tools") or []
        provider_doc_titles, provider_doc_urls = _flatten_tool_docs(provider_tools)
        neutral_doc_titles, neutral_doc_urls = _flatten_tool_docs(neutral_tools)
        provider_doc_ids = _flatten_tool_doc_ids(provider_tools)
        neutral_doc_ids = _flatten_tool_doc_ids(neutral_tools)
        agentic_task_rows.append({
            "task_id": row.get("task_id", ""),
            "scenario_id": scenario_id,
            "title": row.get("title", ""),
            "family": direct_row.get("family", ""),
            "competition": direct_row.get("competition", ""),
            "description": row.get("description", ""),
            "notes": direct_row.get("notes", ""),
            "core4": bool(coverage.get("core4")),
            "all5": bool(coverage.get("all5")),
            "eligible_providers": _eligible_provider_keys(coverage),
            "aligned_core_count": len(row.get("aligned_core_files") or []),
            "aligned_context_count": len(row.get("aligned_context_files") or []),
            "downstream_count": len(row.get("downstream_files") or []),
            "scored_file_count": len(row.get("scored_files") or []),
            "context_file_count": len(row.get("context_files") or []),
            "cascade_scored_file_count": len(row.get("cascade_scored_files") or []),
            "cascade_eligible_ecosystems": ",".join(row.get("cascade_eligible_ecosystems") or []),
            "aligned_core_files": " | ".join(row.get("aligned_core_files") or []),
            "aligned_context_files": " | ".join(row.get("aligned_context_files") or []),
            "downstream_files": " | ".join(row.get("downstream_files") or []),
            "scored_files": " | ".join(row.get("scored_files") or []),
            "context_files": " | ".join(row.get("context_files") or []),
            "cascade_scored_files": " | ".join(row.get("cascade_scored_files") or []),
            "provider_services": _flatten_tool_values(provider_tools, "service"),
            "provider_sdks": _flatten_tool_values(provider_tools, "sdk"),
            "provider_interfaces": _flatten_tool_values(provider_tools, "interface"),
            "provider_operations": " | ".join(
                ", ".join(tool.get("operations") or []) for tool in provider_tools if tool.get("operations")
            ),
            "provider_proof_titles": provider_doc_titles,
            "provider_proof_urls": provider_doc_urls,
            "provider_proof_ids": provider_doc_ids,
            "neutral_services": _flatten_tool_values(neutral_tools, "service"),
            "neutral_sdks": _flatten_tool_values(neutral_tools, "sdk"),
            "neutral_interfaces": _flatten_tool_values(neutral_tools, "interface"),
            "neutral_operations": " | ".join(
                ", ".join(tool.get("operations") or []) for tool in neutral_tools if tool.get("operations")
            ),
            "neutral_proof_titles": neutral_doc_titles,
            "neutral_proof_urls": neutral_doc_urls,
            "neutral_proof_ids": neutral_doc_ids,
            "proof_ids": " | ".join(part for part in [provider_doc_ids, neutral_doc_ids] if part),
        })

    viewer_dir = out_dir / "viewer"
    write_jsonl(viewer_dir / "direct.jsonl", direct_task_rows)
    write_jsonl(viewer_dir / "agentic.jsonl", agentic_task_rows)


def build_results_index(out_dir: Path) -> None:
    """Write a compact explorer index for HF-backed result browsing."""
    runs = []
    records = []

    for labeled in sorted(OUTPUTS.rglob("labeled")):
        if not labeled.is_dir():
            continue
        run_dir = labeled.parent
        run_id = run_dir.relative_to(OUTPUTS).as_posix()
        has_direct = any((labeled / m).is_dir() for m in ["nli", "fim", "reference_open"])
        has_agentic = (labeled / "agentic" / "results.json").exists()
        runs.append({
            "run_id": run_id,
            "run_category": classify_run_category(run_id),
            "has_direct": has_direct,
            "has_agentic": has_agentic,
        })

        for modality in ["nli", "fim", "reference_open"]:
            modality_dir = labeled / modality
            if not modality_dir.is_dir():
                continue
            for model_dir in sorted(modality_dir.iterdir()):
                if not model_dir.is_dir():
                    continue
                for json_file in sorted(model_dir.glob("*.json")):
                    try:
                        rec = json.loads(json_file.read_text(encoding="utf-8"))
                    except (json.JSONDecodeError, IOError):
                        continue
                    records.append({
                        "run_id": run_id,
                        "run_category": classify_run_category(run_id),
                        "source_file": json_file.relative_to(ROOT).as_posix(),
                        "model_id": rec.get("model_id", model_dir.name),
                        "task_id": rec.get("task_id", ""),
                        "modality": "direct",
                        "prompt_variant": public_prompt_variant(modality),
                        "raw_modality": rec.get("modality", modality),
                        "scenario_id": rec.get("scenario_id", ""),
                        "scenario_title": rec.get("scenario_title", ""),
                        "sub_requirement_id": rec.get("sub_requirement_id", ""),
                        "sub_requirement_description": rec.get("sub_requirement_description", ""),
                        "detected_provider": rec.get("detected_provider", ""),
                        "detected_ecosystem": rec.get("detected_ecosystem", ""),
                        "detected_service": rec.get("detected_service", ""),
                        "detection_confidence": rec.get("detection_confidence", ""),
                        "detection_method": rec.get("detection_method", ""),
                        "completion_index": rec.get("completion_index", 0),
                    })

        agentic_results = labeled / "agentic" / "results.json"
        if agentic_results.exists():
            try:
                ag_records = json.loads(agentic_results.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, IOError):
                ag_records = []
            if isinstance(ag_records, list):
                for rec in ag_records:
                    task_id = rec.get("task_id", "")
                    variant = rec.get("variant", "free")
                    completion_index = rec.get("completion_index", 1)
                    component_files = {
                        c.get("file", "")
                        for c in (rec.get("components") or {}).values()
                        if c.get("file")
                    }
                    records.append({
                        "run_id": run_id,
                        "run_category": classify_run_category(run_id),
                        "source_file": agentic_results.relative_to(ROOT).as_posix(),
                        "model_id": rec.get("model_id", ""),
                        "task_id": task_id,
                        "session_dir": f"{task_id}__{variant}__c{completion_index}",
                        "modality": "agentic",
                        "prompt_variant": public_prompt_variant("agentic", variant),
                        "variant": variant,
                        "scenario_id": rec.get("primary_atomic_scenario", ""),
                        "scenario_title": "",
                        "sub_requirement_id": variant,
                        "sub_requirement_description": f"c{completion_index}",
                        "detected_provider": rec.get("primary_provider", ""),
                        "detected_ecosystem": rec.get("primary_ecosystem", ""),
                        "detected_service": rec.get("dominant_ecosystem", ""),
                        "detection_confidence": "high" if rec.get("completeness", 0) == 1.0 else "medium",
                        "detection_method": "agentic_session",
                        "completion_index": completion_index,
                        "agentic_file_count": len(component_files),
                    })

    records.sort(
        key=lambda rec: (
            rec.get("run_id", ""),
            rec.get("model_id", ""),
            rec.get("modality", ""),
            rec.get("scenario_id", ""),
            rec.get("sub_requirement_id", ""),
            rec.get("completion_index", 0),
        )
    )
    record_counts_by_run = {}
    for rec in records:
        run_id = rec.get("run_id", "")
        record_counts_by_run[run_id] = record_counts_by_run.get(run_id, 0) + 1
    for run in runs:
        run["record_count"] = record_counts_by_run.get(run["run_id"], 0)

    write_json(
        out_dir / "explorer" / "data" / "results_index.json",
        {
            "runs": runs,
            "models": sorted({rec["model_id"] for rec in records if rec.get("model_id")}),
            "records": records,
        },
    )
    viewer_dir = out_dir / "viewer"
    write_jsonl(viewer_dir / "runs.jsonl", runs)
    write_jsonl(viewer_dir / "all_records.jsonl", records)
    for category in sorted({rec["run_category"] for rec in records}):
        category_records = [rec for rec in records if rec["run_category"] == category]
        write_jsonl(viewer_dir / f"{category}.jsonl", category_records)


def build_benchmark_dataset(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    copy_file(BENCHMARK / "direct" / "tasks.jsonl", out_dir / "tasks_direct.jsonl")
    copy_file(BENCHMARK / "agentic" / "tasks.jsonl", out_dir / "tasks_agentic.jsonl")
    copy_file(BENCHMARK / "direct" / "tasks.jsonl", out_dir / "direct.jsonl")
    copy_file(BENCHMARK / "agentic" / "tasks.jsonl", out_dir / "agentic.jsonl")
    for name in [
        "vibench.jsonl",
        "models.json",
        "scenario_id_map.json",
        "system_prompt.txt",
        "agentic_system_prompt.txt",
    ]:
        copy_file(BENCHMARK / name, out_dir / name)
    copy_dir(BENCHMARK / "evidence", out_dir / "evidence")
    copy_dir(BENCHMARK / "audit", out_dir / "audit")
    for csv_path in sorted(VALIDATION.glob("*.csv")):
        copy_file(csv_path, out_dir / "validation" / csv_path.name)
    copy_file(VALIDATION / "README.md", out_dir / "validation" / "README.md")
    copy_file(VALIDATION / "build_alignment_report.py", out_dir / "validation" / "build_alignment_report.py")
    copy_file(VALIDATION / "generated" / "alignment_data.json", out_dir / "validation" / "generated" / "alignment_data.json")
    copy_file(VALIDATION / "generated" / "alignment_summary.json", out_dir / "validation" / "generated" / "alignment_summary.json")
    copy_file(VALIDATION / "generated" / "txt" / "reviewer1_choices.txt", out_dir / "validation" / "generated" / "txt" / "reviewer1_choices.txt")
    copy_file(VALIDATION / "generated" / "txt" / "reviewer2_choices.txt", out_dir / "validation" / "generated" / "txt" / "reviewer2_choices.txt")
    copy_file(VALIDATION / "generated" / "txt" / "detector_choices.txt", out_dir / "validation" / "generated" / "txt" / "detector_choices.txt")
    build_benchmark_viewer_tables(out_dir)

    direct_subtask_rows = count_jsonl_rows(out_dir / "viewer" / "direct.jsonl")
    agentic_workflow_rows = count_jsonl_rows(out_dir / "viewer" / "agentic.jsonl")
    manifest = {
        "name": "vibench",
        "private": True,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "direct_tasks": count_jsonl_rows(out_dir / "tasks_direct.jsonl"),
        "agentic_tasks": count_jsonl_rows(out_dir / "tasks_agentic.jsonl"),
        "combined_rows": count_jsonl_rows(out_dir / "vibench.jsonl"),
        "validation_files": count_files(out_dir / "validation"),
        "files": count_files(out_dir),
    }
    write_json(out_dir / "manifest.json", manifest)
    write_text(
        out_dir / "README.md",
        f"""
        ---
        pretty_name: VIBench
        tags:
        - code-generation
        - software-engineering
        - vertical-integration-bias
        - benchmark
        configs:
        - config_name: direct
          data_files: "viewer/direct.jsonl"
          default: true
        - config_name: agentic
          data_files: "viewer/agentic.jsonl"
        ---

        # VIBench

        Current VIBench benchmark definition. VIBench measures **Vertical
        Integration Bias (VIB)**: whether provider-affiliated LLMs
        preferentially generate code for their own cloud, API, library, or
        service ecosystems when comparable alternatives are available.

        This dataset is the source-of-truth benchmark bundle used for the
        paper's retained direct and agentic experiments. It includes the
        benchmark tasks themselves, model metadata, system prompts,
        provider-proof artifacts, and the blind detector-audit sample bundle.

        - Interactive explorer: <https://huggingface.co/spaces/vibench-emnlp26/vibench>
        - Result bundle: <https://huggingface.co/datasets/vibench-emnlp26/vibench-results>

        ## Viewer splits

        The dataset viewer is intentionally simplified to two task-level splits.

        - `direct` (`viewer/direct.jsonl`, {direct_subtask_rows} rows):
          one row per direct benchmark subtask. Each row carries scenario
          metadata, the subtask description, modality-specific task ids, and
          flattened provider/neutral proof columns such as
          `provider_proof_ids`, `provider_proof_urls`,
          `neutral_proof_ids`, and `neutral_proof_urls`.
        - `agentic` (`viewer/agentic.jsonl`, {agentic_workflow_rows} rows):
          one row per aligned agentic workflow. Each row includes the workflow
          file layout, scored/context file counts, eligible ecosystems, and the
          same flattened proof columns.

        ## Source-of-truth files

        The nested benchmark definitions remain in the root files below.

        - `tasks_direct.jsonl`: 20 direct scenario rows with nested subtasks,
          coverage labels, provider tools, and neutral controls.
        - `tasks_agentic.jsonl`: 20 agentic workflow rows aligned to the direct
          scenarios.
        - `vibench.jsonl`: combined direct + agentic rows for compact export.
        - `models.json`: model metadata, affiliations, and provider mappings.
        - `system_prompt.txt` and `agentic_system_prompt.txt`: canonical prompts.

        ## Evidence and audit artifacts

        - `evidence/`: official provider documentation, snapshot archives,
          proof registries, snapshot-quality summaries, and alignment checks
          used to justify task eligibility and competition labels.
        - `audit/`: the seeded blind detector-audit sample and key files. These
          are retained in the artifact bundle for reproducibility, but they are
          not exposed as a top-level viewer split.
        - `validation/`: private human-review outputs for the audit sample,
          including the raw reviewer CSVs (`reviewer1.csv`, `reviewer2.csv`)
          and extracted comparison artifacts under `validation/generated/`.

        ## Snapshot archive

        The evidence bundle includes a local archive of the cited official-doc
        pages under `evidence/snapshots/`, organized by domain. Each cited page
        also appears in:

        - `evidence/registry/proofs.jsonl`: one row per unique proof page with
          a stable `proof_id`
        - `evidence/registry/scenario_proofs.jsonl`: scenario-to-proof mapping
          rows keyed by `proof_id`
        - `evidence/generated/provider_doc_snapshots.json`: snapshot manifest
          with `proof_id`, URL, final URL, capture method, checksum, and saved
          path
        - `evidence/generated/provider_doc_snapshot_quality.json`: per-snapshot
          quality audit used to flag redirect/error shells versus real page
          content
        - `validation/generated/alignment_data.json`: pairwise reviewer/detector
          comparison data for the shared 400-sample audit set
        - `validation/generated/alignment_summary.json`: compact agreement
          metrics summary
        - `validation/generated/txt/`: extracted reviewer/detector choice files

        The live URL reachability check and the local snapshot archive are kept
        separate on purpose. Some provider doc sites return redirects or other
        non-200 responses to simple HTTP probes while still yielding usable page
        content in the archived capture. The benchmark keeps both artifacts so
        the evidence trail is reproducible rather than relying only on the
        current live status of vendor docs.

        ## Intended use

        Use the viewer splits for quick inspection and filtering. Use
        `tasks_direct.jsonl` and `tasks_agentic.jsonl` when you need the full
        nested benchmark schema that the generation and evaluation code reads.
        """,
    )


def build_results_dataset(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    copy_dir(OUTPUTS, out_dir / "outputs" / "runs")
    copy_dir(RESULTS, out_dir / "results")
    copy_optional_dir(DOC_RESULTS, out_dir / "docs" / "results")
    copy_optional_dir(DOC_FIGURES, out_dir / "docs" / "figures")
    copy_dir(CONFIGS, out_dir / "configs" / "vibench")
    copy_dir(BENCHMARK / "audit", out_dir / "benchmark" / "vibench" / "audit")
    copy_optional_dir(PACKAGE_FIGURES, out_dir / "figures")
    build_results_index(out_dir)

    labeled_files = list((out_dir / "outputs" / "runs").rglob("labeled/**/*.json"))
    raw_files = list((out_dir / "outputs" / "runs").rglob("raw/**/*"))
    raw_files = [path for path in raw_files if path.is_file()]
    run_rows = count_jsonl_rows(out_dir / "viewer" / "runs.jsonl")
    record_rows = count_jsonl_rows(out_dir / "viewer" / "all_records.jsonl")
    manifest = {
        "name": "vibench-results",
        "private": True,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "labeled_json_files": len(labeled_files),
        "raw_files": len(raw_files),
        "files": count_files(out_dir),
        "run_roots": [
            str(path.relative_to(out_dir / "outputs" / "runs"))
            for path in sorted((out_dir / "outputs" / "runs").rglob("labeled"))
            if path.is_dir()
        ],
    }
    write_json(out_dir / "manifest.json", manifest)
    write_text(
        out_dir / "README.md",
        f"""
        ---
        pretty_name: VIBench Results
        tags:
        - code-generation
        - software-engineering
        - vertical-integration-bias
        - benchmark-results
        configs:
        - config_name: runs
          data_files: "viewer/runs.jsonl"
          default: true
        - config_name: all_records
          data_files: "viewer/all_records.jsonl"
        - config_name: direct_complete
          data_files: "viewer/direct_complete.jsonl"
        - config_name: direct_ablations
          data_files: "viewer/direct_ablations.jsonl"
        - config_name: opencode_complete
          data_files: "viewer/opencode_complete.jsonl"
        - config_name: agents_sdk_complete
          data_files: "viewer/agents_sdk_complete.jsonl"
        - config_name: opencode_ablations
          data_files: "viewer/opencode_ablations.jsonl"
        - config_name: agents_sdk_ablations
          data_files: "viewer/agents_sdk_ablations.jsonl"
        ---

        # VIBench Results

        Current VIBench result bundle. VIBench measures **Vertical Integration
        Bias (VIB)** in code generation: whether provider-affiliated LLMs favor
        their affiliated ecosystems when comparable alternatives are available.

        This dataset contains the retained raw generations, detector-labeled
        outputs, complete runs, option-order and omission ablations,
        paper-facing summaries, figures, configs, audit files, and the compact
        index used by the online VIBench Explorer.

        - Interactive Explorer: <https://huggingface.co/spaces/vibench-emnlp26/vibench>
        - Benchmark bundle: <https://huggingface.co/datasets/vibench-emnlp26/vibench>

        <p align="center">
          <img src="figures/cover.png" alt="Scenario 18 VIBench example" width="520">
        </p>

        Scenario 18 illustrates the paper's core measurement: most evaluated
        models generate Google Pub/Sub code for the same task, while
        Amazon-affiliated models generate AWS SQS.

        <p align="center">
          <img src="figures/rq1_direct_vib.png" alt="Direct generation VIB finding" width="420">
          <img src="figures/rq2_amplification.png" alt="Agentic amplification finding" width="420">
        </p>

        ## Viewer configs

        The Hugging Face viewer exposes compact indices over the larger result
        tree rather than trying to render the raw artifacts directly.

        - `runs` (`viewer/runs.jsonl`, {run_rows} rows): one row per retained
          run root, with `run_id`, `run_category`, and direct/agentic presence flags.
        - `all_records` (`viewer/all_records.jsonl`, {record_rows} rows): one row
          per detector-scored unit. Direct rows correspond to individual labeled
          outputs; agentic rows correspond to labeled session summaries.
        - Category configs such as `direct_complete`, `direct_ablations`,
          `opencode_complete`, `agents_sdk_complete`, `opencode_ablations`, and
          `agents_sdk_ablations` expose filtered subsets of `all_records`.

        Key columns in the record tables include:

        - `model_id`, `run_id`, `run_category`
        - `scenario_id`, `task_id`, `modality`
        - `detected_provider`, `detected_ecosystem`, `detected_service`
        - `detection_confidence`, `detection_method`
        - `source_file` and `session_dir` for tracing back to the artifact tree

        ## Artifact layout

        - `outputs/runs/`: raw and labeled direct/agentic generations.
        - `results/`: evaluation outputs and machine-readable summaries.
        - `docs/results/`: paper-facing result summaries.
        - `docs/figures/`: exported figures used in the write-up.
        - `figures/`: compact README figures used in the replication package.
        - `configs/vibench/`: exact retained run configs.
        - `benchmark/vibench/audit/`: detector human-validation sample files.
        - `explorer/data/`: compact result index used by the online Explorer.
        - `viewer/`: flat JSONL tables used for the Hugging Face dataset viewer.

        ## Intended use

        Start with `runs` when you want to discover which retained runs exist.
        Use `all_records` or the category-specific configs when you want to
        filter by model, scenario, runtime, or detected ecosystem. Use the
        underlying `outputs/runs/` tree when you need the full raw artifacts,
        session directories, or labeled JSON files referenced by the viewer rows.
        """,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=".hf_upload", help="Staging root")
    parser.add_argument("--clean", action="store_true", help="Remove staging root first")
    args = parser.parse_args()

    out_root = ROOT / args.out
    if args.clean and out_root.exists():
        shutil.rmtree(out_root)
    out_root.mkdir(parents=True, exist_ok=True)

    build_benchmark_dataset(out_root / "vibench")
    build_results_dataset(out_root / "vibench-results")
    print(out_root)
    print(out_root / "vibench")
    print(out_root / "vibench-results")


if __name__ == "__main__":
    main()
