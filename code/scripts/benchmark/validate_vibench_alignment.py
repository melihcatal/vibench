#!/usr/bin/env python3
"""
Validate current VIBench benchmark alignment after scenario reordering.

Checks:
- direct/tasks.jsonl order and schema alignment
- agentic/tasks.jsonl direct-to-agentic mapping
- vibench.jsonl consistency
- provider_tools_and_proofs.json consistency with direct rows
- provider_card_line_audit.json consistency with provider cards
- provider URL index/check artifacts
- explorer benchmark snapshot consistency
- labeled direct and agentic output coverage

Usage:
  python scripts/benchmark/validate_vibench_alignment.py
  python scripts/benchmark/validate_vibench_alignment.py --json-out benchmark/vibench/evidence/generated/alignment_check_summary.json --md-out benchmark/vibench/evidence/generated/alignment_check_report.md
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = BASE_DIR / "benchmark" / "vibench" / "evidence"
GENERATED_DIR = EVIDENCE_DIR / "generated"
REGISTRY_DIR = EVIDENCE_DIR / "registry"

DIRECT_TASKS = BASE_DIR / "benchmark" / "vibench" / "direct" / "tasks.jsonl"
AGENTIC_TASKS = BASE_DIR / "benchmark" / "vibench" / "agentic" / "tasks.jsonl"
COMBINED_TASKS = BASE_DIR / "benchmark" / "vibench" / "vibench.jsonl"
PROOF_FILE = EVIDENCE_DIR / "provider_tools_and_proofs.json"
PROOF_REGISTRY_FILE = REGISTRY_DIR / "proofs.jsonl"
SCENARIO_PROOF_FILE = REGISTRY_DIR / "scenario_proofs.jsonl"
LINE_AUDIT_FILE = GENERATED_DIR / "provider_card_line_audit.json"
URLS_FILE = EVIDENCE_DIR / "provider_urls.txt"
URL_CHECK_FILE = GENERATED_DIR / "provider_url_check.tsv"
URL_CHECK_SUMMARY = GENERATED_DIR / "provider_url_check_summary.json"
SNAPSHOT_MANIFEST = GENERATED_DIR / "provider_doc_snapshots.json"
SNAPSHOT_SUMMARY = GENERATED_DIR / "provider_doc_snapshots_summary.json"
SNAPSHOT_QUALITY = GENERATED_DIR / "provider_doc_snapshot_quality.json"
SNAPSHOT_QUALITY_SUMMARY = GENERATED_DIR / "provider_doc_snapshot_quality_summary.json"
SNAPSHOT_ROOT = EVIDENCE_DIR
EXPLORER_BENCHMARK = BASE_DIR / "vibench-explorer" / "data" / "benchmark.json"
DIRECT_RUN_RESULTS = BASE_DIR / "outputs" / "runs" / "direct" / "complete" / "full_5c" / "labeled"
AGENTIC_RESULTS = BASE_DIR / "outputs" / "runs" / "agentic" / "complete" / "opencode_full_5c" / "labeled" / "agentic" / "results.json"


def _load_json(path: Path):
    return json.loads(path.read_text())


def _load_jsonl(path: Path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def _stable_provider_view(tool: dict) -> dict:
    return {
        "provider_key": tool.get("provider_key"),
        "ecosystem": tool.get("ecosystem"),
        "label": tool.get("label"),
        "service": tool.get("service"),
        "sdk": tool.get("sdk"),
        "interface": tool.get("interface"),
        "eligible": tool.get("eligible"),
        "proof_ids": tool.get("proof_ids", []),
        "official_docs": [
            {
                "url": doc.get("url"),
                "proof_id": doc.get("proof_id"),
            }
            for doc in tool.get("official_docs", [])
        ],
    }


def _compare_provider_lists(left: list[dict], right: list[dict]) -> bool:
    return [_stable_provider_view(item) for item in left] == [
        _stable_provider_view(item) for item in right
    ]


def _eligible_prompt_card_order(row: dict) -> list[str]:
    cards = []
    for tool in row.get("provider_tools", []):
        if tool.get("eligible", True):
            cards.append(tool.get("provider_key"))
    for tool in row.get("neutral_tools", []):
        if tool.get("eligible", True):
            cards.append(tool.get("provider_key"))
    return cards


def _compare_explorer_scenario(source_direct: dict, source_agentic: dict, explorer: dict) -> list[str]:
    errors = []
    if explorer.get("scenario_id") != source_direct.get("scenario_id"):
        errors.append("scenario_id mismatch")
    if explorer.get("title") != source_direct.get("title"):
        errors.append("title mismatch")
    if explorer.get("family") != source_direct.get("family"):
        errors.append("family mismatch")
    if explorer.get("coverage") != source_direct.get("coverage"):
        errors.append("coverage mismatch")
    if not _compare_provider_lists(explorer.get("provider_tools", []), source_direct.get("provider_tools", [])):
        errors.append("provider_tools mismatch")
    if not _compare_provider_lists(explorer.get("neutral_tools", []), source_direct.get("neutral_tools", [])):
        errors.append("neutral_tools mismatch")
    if source_agentic:
        agentic = explorer.get("agentic", {})
        if agentic.get("task_id") != source_agentic.get("task_id"):
            errors.append("agentic task_id mismatch")
        if agentic.get("aligned_core_files") != source_agentic.get("aligned_core_files"):
            errors.append("aligned_core_files mismatch")
        if agentic.get("downstream_files") != source_agentic.get("downstream_files"):
            errors.append("downstream_files mismatch")
    return errors


def validate() -> tuple[dict, list[str]]:
    errors: list[str] = []
    notes: list[str] = []

    direct_rows = _load_jsonl(DIRECT_TASKS)
    agentic_rows = _load_jsonl(AGENTIC_TASKS)
    combined_rows = _load_jsonl(COMBINED_TASKS)
    proof = _load_json(PROOF_FILE)
    proof_registry = _load_jsonl(PROOF_REGISTRY_FILE)
    scenario_proofs = _load_jsonl(SCENARIO_PROOF_FILE)
    line_audit = _load_json(LINE_AUDIT_FILE)
    explorer = _load_json(EXPLORER_BENCHMARK)
    agentic_results = _load_json(AGENTIC_RESULTS)

    direct_order = [row["scenario_id"] for row in direct_rows]
    expected_scenarios = direct_order
    agentic_order = [row["primary_atomic_scenario"] for row in agentic_rows]
    proof_order = [row["scenario_id"] for row in proof["scenarios"]]
    audit_order = [row["scenario_id"] for row in line_audit]
    combined_direct_order = [
        row["scenario_id"]
        for row in combined_rows
        if row.get("dataset_kind") == "direct_hf"
    ]
    combined_agentic_order = [
        row["primary_atomic_scenario"]
        for row in combined_rows
        if row.get("dataset_kind") == "agentic_hf"
    ]
    explorer_order = [row["scenario_id"] for row in explorer.get("scenarios", [])]

    if expected_scenarios != [f"S{i:02d}" for i in range(1, len(expected_scenarios) + 1)]:
        errors.append(f"Direct scenario IDs are not contiguous current IDs: {expected_scenarios}")
    if agentic_order != expected_scenarios:
        errors.append(f"Agentic scenario order mismatch: {agentic_order}")
    if proof_order != expected_scenarios:
        errors.append(f"Proof scenario order mismatch: {proof_order}")
    if audit_order != expected_scenarios:
        errors.append(f"Provider-card audit order mismatch: {audit_order}")
    if combined_direct_order != expected_scenarios:
        errors.append(f"Combined direct order mismatch: {combined_direct_order}")
    if combined_agentic_order != expected_scenarios:
        errors.append(f"Combined agentic order mismatch: {combined_agentic_order}")
    if explorer_order != expected_scenarios:
        errors.append(f"Explorer order mismatch: {explorer_order}")

    direct_by_id = {row["scenario_id"]: row for row in direct_rows}
    agentic_by_id = {row["primary_atomic_scenario"]: row for row in agentic_rows}
    proof_by_id = {row["scenario_id"]: row for row in proof["scenarios"]}
    audit_by_id = {row["scenario_id"]: row for row in line_audit}
    explorer_by_id = {row["scenario_id"]: row for row in explorer.get("scenarios", [])}

    for sid in expected_scenarios:
        direct = direct_by_id[sid]
        agentic = agentic_by_id[sid]
        proof_row = proof_by_id[sid]
        audit_row = audit_by_id[sid]
        explorer_row = explorer_by_id.get(sid, {})

        if direct.get("title") != proof_row.get("title"):
            errors.append(f"{sid}: title mismatch between direct and proof file")
        if direct.get("family") != proof_row.get("family"):
            errors.append(f"{sid}: family mismatch between direct and proof file")
        if direct.get("coverage") != proof_row.get("coverage"):
            errors.append(f"{sid}: coverage mismatch between direct and proof file")
        if direct.get("provider_proof_ids", []) != proof_row.get("provider_proof_ids", []):
            errors.append(f"{sid}: provider_proof_ids mismatch between direct and proof file")
        if direct.get("neutral_proof_ids", []) != proof_row.get("neutral_proof_ids", []):
            errors.append(f"{sid}: neutral_proof_ids mismatch between direct and proof file")
        if not _compare_provider_lists(direct.get("provider_tools", []), proof_row.get("provider_tools", [])):
            errors.append(f"{sid}: provider_tools mismatch between direct and proof file")
        if not _compare_provider_lists(direct.get("neutral_tools", []), proof_row.get("neutral_tools", [])):
            errors.append(f"{sid}: neutral_tools mismatch between direct and proof file")

        expected_card_order = _eligible_prompt_card_order(direct)
        observed_card_order = [card.get("provider_key") for card in audit_row.get("cards", [])]
        if audit_row.get("title") != direct.get("title"):
            errors.append(f"{sid}: title mismatch between direct and line audit")
        if audit_row.get("option_count") != len(expected_card_order):
            errors.append(f"{sid}: option_count mismatch in provider card audit")
        if observed_card_order != expected_card_order:
            errors.append(f"{sid}: provider card order mismatch")

        if agentic.get("task_id") != f"agentic_{sid}":
            errors.append(f"{sid}: agentic task_id mismatch ({agentic.get('task_id')})")
        if agentic.get("direct_dataset_row_id") != sid:
            errors.append(f"{sid}: direct_dataset_row_id mismatch")
        if agentic.get("primary_atomic_scenario") != sid:
            errors.append(f"{sid}: primary_atomic_scenario mismatch")
        expected_core_files = [sub["file"] for sub in direct.get("subtasks", [])]
        if agentic.get("aligned_core_files") != expected_core_files:
            errors.append(f"{sid}: aligned_core_files mismatch")
        if len(agentic.get("aligned_context_files", [])) != 2:
            errors.append(f"{sid}: expected 2 aligned context files")
        if len(agentic.get("downstream_files", [])) != 4:
            errors.append(f"{sid}: expected 4 downstream files")
        if len(agentic.get("expected_files", [])) != 10:
            errors.append(f"{sid}: expected 10 total files")
        if len(agentic.get("scored_files", [])) != 8:
            errors.append(f"{sid}: expected 8 scored files")

        core_components = [
            comp for comp in agentic.get("components", [])
            if comp.get("component_group") == "aligned_core"
        ]
        if len(core_components) != 4:
            errors.append(f"{sid}: expected 4 aligned-core components")
        else:
            suffixes = ["a", "b", "c", "d"]
            for idx, (subtask, comp, suffix) in enumerate(zip(direct["subtasks"], core_components, suffixes), start=1):
                if comp.get("atomic_scenario") != sid:
                    errors.append(f"{sid}: core component {comp.get('file')} atomic_scenario mismatch")
                if comp.get("file") != subtask.get("file"):
                    errors.append(f"{sid}: core component file mismatch for index {idx}")
                expected_atomic = f"nli_{sid}_{suffix}"
                if comp.get("atomic_subtask_id") != expected_atomic:
                    errors.append(f"{sid}: atomic_subtask_id mismatch for {comp.get('file')}")
                if comp.get("atomic_subtask_index") != idx:
                    errors.append(f"{sid}: atomic_subtask_index mismatch for {comp.get('file')}")

        explorer_mismatches = _compare_explorer_scenario(direct, agentic, explorer_row)
        for mismatch in explorer_mismatches:
            errors.append(f"{sid}: explorer {mismatch}")

    proof_urls = []
    proof_ids = []
    for row in proof["scenarios"]:
        for bucket in ("provider_tools", "neutral_tools"):
            for tool in row.get(bucket, []):
                for doc in tool.get("official_docs", []):
                    proof_urls.append(doc.get("url"))
                    proof_ids.append(doc.get("proof_id"))
    proof_url_set = {url for url in proof_urls if url}
    proof_id_set = {proof_id for proof_id in proof_ids if proof_id}
    if len(proof_id_set) != len(proof_url_set):
        errors.append("Proof IDs are missing or duplicated relative to the unique proof URL set")
    registry_url_set = {row.get("url") for row in proof_registry if row.get("url")}
    registry_id_set = {row.get("proof_id") for row in proof_registry if row.get("proof_id")}
    if registry_url_set != proof_url_set:
        errors.append("registry/proofs.jsonl does not exactly match proof official_docs URL set")
    if registry_id_set != proof_id_set:
        errors.append("registry/proofs.jsonl proof_id set does not exactly match proof official_docs proof_id set")
    scenario_proof_ids = {row.get("proof_id") for row in scenario_proofs if row.get("proof_id")}
    if scenario_proof_ids != proof_id_set:
        errors.append("registry/scenario_proofs.jsonl proof_id set does not cover the proof official_docs proof_id set")
    txt_urls = {line.strip() for line in URLS_FILE.read_text().splitlines() if line.strip()}
    tsv_lines = [line for line in URL_CHECK_FILE.read_text().splitlines() if line.strip()]
    tsv_pairs = []
    for line in tsv_lines:
        if "\t" not in line:
            continue
        code, url = line.split("\t", 1)
        tsv_pairs.append((code, url))
    tsv_urls = {url for _code, url in tsv_pairs}
    url_summary = _load_json(URL_CHECK_SUMMARY)
    snapshot_manifest = _load_json(SNAPSHOT_MANIFEST)
    snapshot_summary = _load_json(SNAPSHOT_SUMMARY)
    snapshot_quality = _load_json(SNAPSHOT_QUALITY)
    snapshot_quality_summary = _load_json(SNAPSHOT_QUALITY_SUMMARY)

    if proof_url_set != txt_urls:
        errors.append("provider_urls.txt does not exactly match proof official_docs URL set")
    if proof_url_set != tsv_urls:
        notes.append("provider_url_check.tsv is stale relative to proof official_docs URL set")
    summary_total = sum(int(count) for count in url_summary.values())
    if summary_total != len(proof_url_set):
        notes.append("provider_url_check_summary.json totals are stale relative to the current proof URL set")
    non_200 = {
        code: count
        for code, count in url_summary.items()
        if code != "200"
    }
    non_200_urls = {
        code: sorted(url for status, url in tsv_pairs if status == code)
        for code in sorted(non_200)
    }
    if non_200:
        notes.append(f"Non-200 live proof URLs recorded in summary: {non_200}")

    snapshot_url_set = {entry.get("url") for entry in snapshot_manifest if entry.get("url")}
    if proof_url_set != snapshot_url_set:
        errors.append("provider_doc_snapshots.json does not exactly match proof official_docs URL set")
    snapshot_proof_ids = {entry.get("proof_id") for entry in snapshot_manifest if entry.get("proof_id")}
    if snapshot_proof_ids != proof_id_set:
        errors.append("provider_doc_snapshots.json proof_id set does not exactly match proof official_docs proof_id set")
    missing_snapshot_files = []
    expected_snapshot_relpaths = set()
    snapshot_status_counts = Counter()
    for entry in snapshot_manifest:
        relpath = entry.get("snapshot_relpath")
        if relpath:
            expected_snapshot_relpaths.add(relpath)
            snapshot_path = SNAPSHOT_ROOT / relpath
            if not snapshot_path.exists():
                missing_snapshot_files.append(relpath)
        snapshot_status_counts[str(entry.get("http_status"))] += 1
    if missing_snapshot_files:
        errors.append(f"Snapshot files listed in provider_doc_snapshots.json are missing: {missing_snapshot_files[:10]}")
    actual_snapshot_relpaths = {
        str(path.relative_to(SNAPSHOT_ROOT))
        for path in (SNAPSHOT_ROOT / "snapshots").rglob("*")
        if path.is_file()
    }
    extra_snapshot_files = sorted(actual_snapshot_relpaths - expected_snapshot_relpaths)
    if extra_snapshot_files:
        notes.append(f"Stale extra snapshot files present outside current manifest: {len(extra_snapshot_files)}")
    if int(snapshot_summary.get("snapshot_count", -1)) != len(snapshot_manifest):
        errors.append("provider_doc_snapshots_summary.json snapshot_count does not match manifest length")
    if snapshot_summary.get("status_counts") != dict(sorted(snapshot_status_counts.items())):
        errors.append("provider_doc_snapshots_summary.json status_counts do not match manifest contents")
    snapshot_non_200 = {
        code: count
        for code, count in snapshot_status_counts.items()
        if code != "200"
    }
    if snapshot_non_200:
        notes.append(f"Non-200 snapshot statuses recorded in snapshot manifest: {snapshot_non_200}")
    snapshot_quality_urls = {entry.get("url") for entry in snapshot_quality if entry.get("url")}
    if proof_url_set != snapshot_quality_urls:
        errors.append("provider_doc_snapshot_quality.json does not exactly match proof official_docs URL set")
    snapshot_quality_ids = {entry.get("proof_id") for entry in snapshot_quality if entry.get("proof_id")}
    if snapshot_quality_ids != proof_id_set:
        errors.append("provider_doc_snapshot_quality.json proof_id set does not exactly match proof official_docs proof_id set")
    quality_counts = Counter(entry.get("quality", "unknown") for entry in snapshot_quality)
    if int(snapshot_quality_summary.get("snapshot_count", -1)) != len(snapshot_quality):
        errors.append("provider_doc_snapshot_quality_summary.json snapshot_count does not match quality record length")
    if snapshot_quality_summary.get("quality_counts") != dict(sorted(quality_counts.items())):
        errors.append("provider_doc_snapshot_quality_summary.json quality_counts do not match quality records")
    weak_snapshot_urls = [entry.get("url") for entry in snapshot_quality if entry.get("quality") == "weak" and entry.get("url")]
    review_snapshot_urls = [entry.get("url") for entry in snapshot_quality if entry.get("quality") == "review" and entry.get("url")]
    if snapshot_quality_summary.get("weak_urls") != weak_snapshot_urls:
        errors.append("provider_doc_snapshot_quality_summary.json weak_urls do not match quality records")
    if snapshot_quality_summary.get("review_urls") != review_snapshot_urls:
        errors.append("provider_doc_snapshot_quality_summary.json review_urls do not match quality records")
    if weak_snapshot_urls:
        notes.append(f"Weak snapshot captures detected: {len(weak_snapshot_urls)}")
    if review_snapshot_urls:
        notes.append(f"Review-needed snapshot captures detected: {len(review_snapshot_urls)}")

    direct_records = []
    for modality_dir in sorted(DIRECT_RUN_RESULTS.iterdir()):
        if not modality_dir.is_dir():
            continue
        for json_file in modality_dir.rglob("*.json"):
            try:
                direct_records.append(_load_json(json_file))
            except json.JSONDecodeError:
                errors.append(f"Unreadable direct labeled file: {json_file}")

    direct_scenarios = [row.get("scenario_id") for row in direct_records if row.get("scenario_id")]
    direct_counts = Counter(direct_scenarios)
    direct_missing = [sid for sid in expected_scenarios if sid not in direct_counts]
    direct_extra = [sid for sid in sorted(direct_counts) if sid not in expected_scenarios]
    if direct_extra:
        errors.append(f"Direct labeled scenario coverage has unexpected extra scenarios: {direct_extra}")
    if direct_missing:
        notes.append(f"Direct labeled outputs are missing current benchmark scenarios: {direct_missing}")
    if len(set(direct_counts.values())) != 1:
        notes.append(f"Direct labeled counts are non-uniform: {dict(sorted(direct_counts.items()))}")

    agentic_task_counts = Counter(row.get("task_id") for row in agentic_results if row.get("task_id"))
    agentic_scenario_counts = Counter(
        row.get("primary_atomic_scenario")
        for row in agentic_results
        if row.get("primary_atomic_scenario")
    )
    expected_agentic_tasks = [f"agentic_{sid}" for sid in expected_scenarios]
    agentic_missing_tasks = [task_id for task_id in expected_agentic_tasks if task_id not in agentic_task_counts]
    agentic_extra_tasks = [task_id for task_id in sorted(agentic_task_counts) if task_id not in expected_agentic_tasks]
    agentic_missing_scenarios = [sid for sid in expected_scenarios if sid not in agentic_scenario_counts]
    agentic_extra_scenarios = [sid for sid in sorted(agentic_scenario_counts) if sid not in expected_scenarios]
    if agentic_extra_tasks:
        errors.append(f"Agentic labeled task coverage has unexpected extra tasks: {agentic_extra_tasks}")
    if agentic_extra_scenarios:
        errors.append(f"Agentic labeled scenario coverage has unexpected extra scenarios: {agentic_extra_scenarios}")
    if agentic_missing_tasks:
        notes.append(f"Agentic labeled outputs are missing current benchmark tasks: {agentic_missing_tasks}")
    if agentic_missing_scenarios:
        notes.append(f"Agentic labeled outputs are missing current benchmark scenarios: {agentic_missing_scenarios}")
    if len(set(agentic_task_counts.values())) != 1:
        errors.append(f"Agentic labeled task counts are non-uniform: {dict(sorted(agentic_task_counts.items()))}")
    if len(set(agentic_scenario_counts.values())) != 1:
        errors.append(f"Agentic labeled scenario counts are non-uniform: {dict(sorted(agentic_scenario_counts.items()))}")

    summary = {
        "status": "pass" if not errors else "fail",
        "expected_scenarios": expected_scenarios,
        "direct_order": direct_order,
        "agentic_order": agentic_order,
        "proof_order": proof_order,
        "provider_card_audit_order": audit_order,
        "combined_direct_order": combined_direct_order,
        "combined_agentic_order": combined_agentic_order,
        "explorer_order": explorer_order,
        "proof_url_unique_count": len(proof_url_set),
        "proof_id_unique_count": len(proof_id_set),
        "proof_registry_count": len(proof_registry),
        "scenario_proof_link_count": len(scenario_proofs),
        "provider_urls_txt_count": len(txt_urls),
        "provider_url_check_tsv_count": len(tsv_urls),
        "provider_url_http_200_count": url_summary.get("200", 0),
        "provider_url_non_200_urls": non_200_urls,
        "provider_doc_snapshot_count": len(snapshot_manifest),
        "provider_doc_snapshot_status_counts": dict(sorted(snapshot_status_counts.items())),
        "provider_doc_snapshot_quality_counts": dict(sorted(quality_counts.items())),
        "provider_doc_snapshot_weak_urls": weak_snapshot_urls,
        "provider_doc_snapshot_review_urls": review_snapshot_urls,
        "direct_labeled_total": len(direct_records),
        "direct_labeled_scenario_counts": dict(sorted(direct_counts.items())),
        "agentic_labeled_total": len(agentic_results),
        "agentic_labeled_task_counts": dict(sorted(agentic_task_counts.items())),
        "agentic_labeled_scenario_counts": dict(sorted(agentic_scenario_counts.items())),
        "error_count": len(errors),
        "note_count": len(notes),
        "errors": errors,
        "notes": notes,
    }
    return summary, errors


def _markdown_report(summary: dict) -> str:
    lines = [
        "# VIBench Alignment Check",
        "",
        f"- Status: `{summary['status']}`",
        f"- Error count: `{summary['error_count']}`",
        f"- Note count: `{summary['note_count']}`",
        "",
        "## Orders",
        "",
        f"- Direct: `{summary['direct_order']}`",
        f"- Agentic: `{summary['agentic_order']}`",
        f"- Proof: `{summary['proof_order']}`",
        f"- Provider card audit: `{summary['provider_card_audit_order']}`",
        f"- Combined direct: `{summary['combined_direct_order']}`",
        f"- Combined agentic: `{summary['combined_agentic_order']}`",
        f"- Explorer: `{summary['explorer_order']}`",
        "",
        "## Proof URL Index",
        "",
        f"- Unique proof URLs: `{summary['proof_url_unique_count']}`",
        f"- Unique proof IDs: `{summary['proof_id_unique_count']}`",
        f"- `registry/proofs.jsonl`: `{summary['proof_registry_count']}`",
        f"- `registry/scenario_proofs.jsonl`: `{summary['scenario_proof_link_count']}`",
        f"- `provider_urls.txt`: `{summary['provider_urls_txt_count']}`",
        f"- `provider_url_check.tsv`: `{summary['provider_url_check_tsv_count']}`",
        f"- Saved HTTP 200 count: `{summary['provider_url_http_200_count']}`",
        f"- `provider_doc_snapshots.json`: `{summary['provider_doc_snapshot_count']}`",
        f"- Snapshot status counts: `{summary['provider_doc_snapshot_status_counts']}`",
        f"- Snapshot quality counts: `{summary['provider_doc_snapshot_quality_counts']}`",
        "",
    ]
    non_200_urls = summary.get("provider_url_non_200_urls") or {}
    if non_200_urls:
        lines.extend(["### Non-200 proof URLs", ""])
        for code, urls in non_200_urls.items():
            lines.append(f"- {code}:")
            for url in urls:
                lines.append(f"  - `{url}`")
        lines.append("")
    weak_snapshot_urls = summary.get("provider_doc_snapshot_weak_urls") or []
    review_snapshot_urls = summary.get("provider_doc_snapshot_review_urls") or []
    if weak_snapshot_urls:
        lines.extend(["### Weak snapshots", ""])
        for url in weak_snapshot_urls:
            lines.append(f"- `{url}`")
        lines.append("")
    if review_snapshot_urls:
        lines.extend(["### Review-needed snapshots", ""])
        for url in review_snapshot_urls:
            lines.append(f"- `{url}`")
        lines.append("")
    lines.extend([
        "## Output Coverage",
        "",
        f"- Direct labeled total: `{summary['direct_labeled_total']}`",
        f"- Agentic labeled total: `{summary['agentic_labeled_total']}`",
        "",
        "### Direct scenario counts",
        "",
    ])
    for sid, count in summary["direct_labeled_scenario_counts"].items():
        lines.append(f"- {sid}: `{count}`")
    lines.extend(["", "### Agentic task counts", ""])
    for task_id, count in summary["agentic_labeled_task_counts"].items():
        lines.append(f"- {task_id}: `{count}`")
    lines.extend(["", "### Agentic scenario counts", ""])
    for sid, count in summary["agentic_labeled_scenario_counts"].items():
        lines.append(f"- {sid}: `{count}`")

    if summary["errors"]:
        lines.extend(["", "## Errors", ""])
        for error in summary["errors"]:
            lines.append(f"- {error}")
    if summary["notes"]:
        lines.extend(["", "## Notes", ""])
        for note in summary["notes"]:
            lines.append(f"- {note}")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Validate VIBench v3 alignment")
    parser.add_argument("--json-out", type=Path, default=None)
    parser.add_argument("--md-out", type=Path, default=None)
    args = parser.parse_args()

    summary, errors = validate()
    print(json.dumps(summary, indent=2))

    if args.json_out:
        args.json_out.write_text(json.dumps(summary, indent=2) + "\n")
    if args.md_out:
        args.md_out.write_text(_markdown_report(summary))

    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
