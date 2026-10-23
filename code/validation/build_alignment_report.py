from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = BASE_DIR.parent
VALIDATION_DIR = BASE_DIR / "validation"
DEFAULT_OUT_DIR = VALIDATION_DIR / "generated"
MAX_OUTPUT = 3000

sys.path.insert(0, str(BASE_DIR / "scripts" / "audit"))
sys.path.insert(0, str(BASE_DIR / "scripts" / "evaluation" / "core"))

from generate_audit_sample import _discover_current_runs, load_agentic_pool, load_direct_pool  # noqa: E402
from evaluate_agentic import (  # noqa: E402
    _component_is_scored,
    detect_provider_from_file,
    propagate_local_dependency_detections,
    resolve_primary_component,
)


def _truncate(text: str, limit: int) -> str:
    if not text:
        return ""
    return text if len(text) <= limit else text[:limit] + "\n... [truncated]"


def load_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def normalize_text(value: str | None) -> str:
    return (value or "").strip()


def normalize_label(value: str | None) -> str:
    return normalize_text(value).lower()


def canonical_label(label: str | None, other_label: str | None = None) -> str:
    base = normalize_label(label)
    if not base:
        return ""
    if base == "other":
        detail = normalize_label(other_label)
        return f"other:{detail}" if detail else "other"
    return base


def display_label(label: str | None, other_label: str | None = None) -> str:
    base = normalize_label(label)
    if not base:
        return ""
    if base == "other":
        detail = normalize_text(other_label)
        return detail or "other"
    return base


def label_family(canonical: str) -> str:
    if canonical.startswith("other:"):
        return "other"
    return canonical


def sample_id_for_pool_row(row: dict[str, Any]) -> str:
    raw = json.dumps(
        [
            row.get("run_id", ""),
            row.get("source", ""),
            row.get("model_id", ""),
            row.get("task_id", ""),
            row.get("modality", ""),
            row.get("component_file", ""),
            row.get("source_path", ""),
        ],
        separators=(",", ":"),
    )
    return hashlib.sha256(raw.encode()).hexdigest()[:12]


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


# The config-variant runs were once filed under outputs/runs/<mode>/ablations/
# and are now under <mode>/variants/. A sample id hashes the run path, and the
# shipped n=400 sample and both reviewer CSVs key off those ids, so the ids must
# stay fixed across that rename: match a row under its current path and under
# the one in force when the sample was drawn.
_LEGACY_RUN_SEGMENTS = [("/variants/", "/ablations/")]


def _candidate_sample_ids(row: dict[str, Any]) -> list[str]:
    ids = [sample_id_for_pool_row(row)]
    for current, legacy in _LEGACY_RUN_SEGMENTS:
        run_id = normalize_text(row.get("run_id"))
        source_path = normalize_text(row.get("source_path"))
        if current.strip("/") not in run_id and current not in source_path:
            continue
        aliased = dict(row)
        aliased["run_id"] = run_id.replace(current.strip("/"), legacy.strip("/"))
        aliased["source_path"] = source_path.replace(current, legacy)
        ids.append(sample_id_for_pool_row(aliased))
    return ids


def _build_locator_rows(sample_ids: set[str]) -> dict[str, dict[str, Any]]:
    locator_rows: dict[str, dict[str, Any]] = {}
    for run in _discover_current_runs():
        for pool in (load_direct_pool(run),
                     load_agentic_pool(run, include_unscored=False)):
            for row in pool:
                for sample_id in _candidate_sample_ids(row):
                    if sample_id in sample_ids:
                        enriched = dict(row)
                        enriched["sample_id"] = sample_id
                        locator_rows[sample_id] = enriched
                        break

    missing = sorted(sample_ids - set(locator_rows))
    if missing:
        raise RuntimeError(
            f"Failed to reconstruct {len(missing)} sample ids from current retained runs. "
            f"First missing ids: {missing[:10]}"
        )
    return locator_rows


def _recompute_agentic_session(locator_row: dict[str, Any]) -> dict[str, dict[str, Any]]:
    source_rel = normalize_text(locator_row.get("source_path"))
    source_path = REPO_ROOT / source_rel
    session_dir = source_path.parent
    meta_path = session_dir / "_meta.json"
    if not meta_path.exists():
        raise RuntimeError(f"Missing _meta.json for agentic sample: {source_rel}")

    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    primary_component = resolve_primary_component(meta)
    primary_file = primary_component.get("file") if primary_component else None
    scored_files = set(meta.get("scored_files", []))
    seed_files = meta.get("seed_files", []) or []
    seeded_file_names = {
        seed.get("file")
        for seed in seed_files
        if isinstance(seed, dict) and seed.get("file")
    }

    detected: dict[str, dict[str, Any]] = {}
    file_contents: dict[str, str] = {}
    for comp in meta["components"]:
        fname = comp["file"]
        role = comp["role"]
        fpath = session_dir / fname

        if fpath.exists():
            content = fpath.read_text(encoding="utf-8")
            file_contents[fname] = content
            detection = detect_provider_from_file(content)
            present = True
        else:
            detection = detect_provider_from_file("")
            present = False

        detected[role] = {
            "file": fname,
            "atomic_scenario": comp["atomic_scenario"],
            "provider": detection["provider"],
            "ecosystem": detection["ecosystem"],
            "service": detection["service"],
            "confidence": detection["confidence"],
            "detected_providers": detection["detected_providers"],
            "detected_ecosystems": detection["detected_ecosystems"],
            "detected_services": detection["detected_services"],
            "detected_methods": detection["detected_methods"],
            "is_multi_provider": detection["is_multi_provider"],
            "is_multi_ecosystem": detection["is_multi_ecosystem"],
            "present": present,
            "is_primary": bool(primary_file and fname == primary_file),
            "is_scored": _component_is_scored(comp, scored_files),
            "is_seeded": fname in seeded_file_names,
            "component_group": comp.get("component_group"),
            "coupling_expectation": comp.get("coupling_expectation"),
            "dependency_reason": comp.get("dependency_reason"),
        }

    for helper_path in session_dir.glob("*.py"):
        fname = helper_path.name
        if fname in file_contents:
            continue
        try:
            file_contents[fname] = helper_path.read_text(encoding="utf-8")
        except OSError:
            continue

    propagate_local_dependency_detections(detected, file_contents)

    session_rows: dict[str, dict[str, Any]] = {}
    for component_key, component in detected.items():
        if not component.get("is_scored"):
            continue
        file_name = component.get("file", "")
        content = _truncate(file_contents.get(file_name, ""), MAX_OUTPUT)
        if not content.strip():
            continue
        file_path = session_dir / file_name
        row = {
            "source": "agentic",
            "run_id": locator_row.get("run_id", ""),
            "source_path": str(file_path.relative_to(REPO_ROOT)),
            "model_id": meta.get("model_id", ""),
            "task_id": meta.get("task_id", ""),
            "modality": f"agentic_{meta.get('variant', '')}",
            "variant": meta.get("variant", ""),
            "scenario_id": meta.get("primary_atomic_scenario", ""),
            "component_key": component_key,
            "component_file": file_name,
            "component_group": component.get("component_group", ""),
            "component_role": component_key,
            "coupling_expectation": component.get("coupling_expectation", ""),
            "is_scored": bool(component.get("is_scored")),
            "output_text": content,
            "detector_provider": component.get("provider", ""),
            "detector_ecosystem": component.get("ecosystem", ""),
            "detector_service": component.get("service", ""),
            "detector_confidence": component.get("confidence", ""),
            "detector_method": ",".join(component.get("detected_methods") or []),
        }
        # Index under every spelling of the id, for the same reason
        # _candidate_sample_ids exists.
        for candidate in _candidate_sample_ids(row):
            session_rows[candidate] = row
    return session_rows


def _recompute_direct_row(locator_row: dict[str, Any]) -> dict[str, Any]:
    content = locator_row.get("output_text", "") or ""
    detection = detect_provider_from_file(content)
    fresh = dict(locator_row)
    fresh["detector_provider"] = detection["provider"]
    fresh["detector_ecosystem"] = detection["ecosystem"]
    fresh["detector_service"] = detection["service"]
    fresh["detector_confidence"] = detection["confidence"]
    fresh["detector_method"] = ",".join(detection.get("detected_methods") or [])
    return fresh


def build_detector_rows(sample_ids: set[str]) -> dict[str, dict[str, Any]]:
    locator_rows = _build_locator_rows(sample_ids)
    detector_rows: dict[str, dict[str, Any]] = {}

    for sample_id, row in locator_rows.items():
        if row.get("source") == "direct":
            detector_rows[sample_id] = _recompute_direct_row(row)

    session_locators: dict[str, list[tuple[str, dict[str, Any]]]] = defaultdict(list)
    for sample_id, row in locator_rows.items():
        if row.get("source") != "agentic":
            continue
        session_key = str((REPO_ROOT / normalize_text(row.get("source_path"))).parent)
        session_locators[session_key].append((sample_id, row))

    for locators in session_locators.values():
        recomputed = _recompute_agentic_session(locators[0][1])
        for sample_id, _locator in locators:
            fresh = recomputed.get(sample_id)
            if fresh:
                fresh["sample_id"] = sample_id
                detector_rows[sample_id] = fresh

    missing = sorted(sample_ids - set(detector_rows))
    if missing:
        raise RuntimeError(
            f"Failed to rebuild detector rows for {len(missing)} sample ids. "
            f"First missing ids: {missing[:10]}"
        )
    return detector_rows


def reviewer_record(row: dict[str, str]) -> dict[str, Any]:
    label = normalize_label(row.get("human_label"))
    other_label = normalize_text(row.get("human_other_label"))
    notes = normalize_text(row.get("notes"))
    return {
        "present": True,
        "label": label,
        "other_label": other_label,
        "notes": notes,
        "canonical": canonical_label(label, other_label),
        "display": display_label(label, other_label),
    }


def detector_record(row: dict[str, Any] | None) -> dict[str, Any]:
    if not row:
        return {
            "present": False,
            "label": "",
            "canonical": "",
            "display": "",
            "provider": "",
            "service": "",
            "confidence": "",
            "source_path": "",
        }
    label = normalize_label(row.get("detector_ecosystem"))
    return {
        "present": True,
        "label": label,
        "canonical": canonical_label(label),
        "display": display_label(label),
        "provider": normalize_text(row.get("detector_provider")),
        "service": normalize_text(row.get("detector_service")),
        "confidence": normalize_text(row.get("detector_confidence")),
        "source_path": normalize_text(row.get("source_path")),
    }


def row_metadata(detector_row: dict[str, Any] | None, fallback_row: dict[str, str] | None) -> dict[str, Any]:
    src = detector_row or fallback_row or {}
    return {
        "source": normalize_text(src.get("source")),
        "model_id": normalize_text(src.get("model_id")),
        "task_id": normalize_text(src.get("task_id")),
        "scenario_id": normalize_text(src.get("scenario_id")),
        "modality": normalize_text(src.get("modality")),
        "component_file": normalize_text(src.get("component_file")),
        "component_group": normalize_text(src.get("component_group")),
        "detector_source_path": normalize_text((detector_row or {}).get("source_path")),
    }


def pair_metrics(rows: list[dict[str, Any]], left_key: str, right_key: str) -> dict[str, Any]:
    compared: list[dict[str, Any]] = []
    confusion: dict[str, Counter[str]] = defaultdict(Counter)
    left_counts: Counter[str] = Counter()
    right_counts: Counter[str] = Counter()
    exact = 0
    exact_known = 0
    exact_determinate = 0
    known_n = 0
    determinate_n = 0

    for row in rows:
        left = row[left_key]
        right = row[right_key]
        if not left.get("present") or not right.get("present"):
            continue
        if not left.get("canonical") or not right.get("canonical"):
            continue

        left_can = left["canonical"]
        right_can = right["canonical"]
        left_disp = left["display"]
        right_disp = right["display"]
        match = left_can == right_can
        if match:
            exact += 1
        compared.append(
            {
                "sample_id": row["sample_id"],
                "sample_index": row["sample_index"],
                "source": row["source"],
                "model_id": row["model_id"],
                "task_id": row["task_id"],
                "scenario_id": row["scenario_id"],
                "modality": row["modality"],
                "component_file": row["component_file"],
                "component_group": row["component_group"],
                "detector_source_path": row["detector_source_path"],
                "left_display": left_disp,
                "right_display": right_disp,
                "left_canonical": left_can,
                "right_canonical": right_can,
                "left_notes": left.get("notes", ""),
                "right_notes": right.get("notes", ""),
                "right_provider": right.get("provider", ""),
                "right_service": right.get("service", ""),
                "right_confidence": right.get("confidence", ""),
                "match": match,
            }
        )
        confusion[left_disp][right_disp] += 1
        left_counts[left_can] += 1
        right_counts[right_can] += 1

        if left_can != "unknown" and right_can != "unknown":
            known_n += 1
            if match:
                exact_known += 1
        if (
            left_can != "unknown"
            and right_can != "unknown"
            and not left_can.startswith("other")
            and not right_can.startswith("other")
        ):
            determinate_n += 1
            if match:
                exact_determinate += 1

    compared_n = len(compared)
    agreement = exact / compared_n if compared_n else None
    agreement_known = exact_known / known_n if known_n else None
    agreement_determinate = exact_determinate / determinate_n if determinate_n else None

    kappa = None
    if compared_n:
        categories = set(left_counts) | set(right_counts)
        po = agreement
        pe = sum(
            (left_counts[c] / compared_n) * (right_counts[c] / compared_n)
            for c in categories
        )
        if (1 - pe) != 0:
            kappa = (po - pe) / (1 - pe)

    disagreements = [row for row in compared if not row["match"]]
    buckets = Counter((row["left_display"], row["right_display"]) for row in disagreements)
    bucket_rows = [
        {"left_display": left, "right_display": right, "count": count}
        for (left, right), count in buckets.most_common()
    ]

    return {
        "compared_count": compared_n,
        "exact_matches": exact,
        "exact_agreement": agreement,
        "agreement_excluding_unknown": agreement_known,
        "agreement_determinate_only": agreement_determinate,
        "cohen_kappa": kappa,
        "left_distribution": dict(sorted(Counter(label_family(x) for x in left_counts.elements()).items())),
        "right_distribution": dict(sorted(Counter(label_family(x) for x in right_counts.elements()).items())),
        "confusion": {left: dict(rights) for left, rights in sorted(confusion.items())},
        "disagreement_buckets": bucket_rows,
        "disagreements": disagreements,
    }


def triad_category(row: dict[str, Any]) -> str:
    r1 = row["reviewer1"]["canonical"]
    r2 = row["reviewer2"]["canonical"]
    det = row["detector"]["canonical"]
    if not r1 or not r2 or not det:
        return ""
    if r1 == r2 == det:
        return "unanimous"
    if r1 == r2:
        return "humans_agree_detector_diff"
    if r1 == det:
        return "reviewer1_detector_agree_reviewer2_diff"
    if r2 == det:
        return "reviewer2_detector_agree_reviewer1_diff"
    return "all_different"


def triad_category_label(category: str) -> str:
    labels = {
        "unanimous": "all three agree",
        "humans_agree_detector_diff": "reviewers agree, detector differs",
        "reviewer1_detector_agree_reviewer2_diff": "reviewer1 + detector agree",
        "reviewer2_detector_agree_reviewer1_diff": "reviewer2 + detector agree",
        "all_different": "all three differ",
    }
    return labels.get(category, category or "unknown")


def triad_metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    compared: list[dict[str, Any]] = []
    unanimous = 0
    majority = 0
    all_different = 0
    known_n = 0
    exact_known = 0
    determinate_n = 0
    exact_determinate = 0
    category_counts: Counter[str] = Counter()

    for row in rows:
        r1 = row["reviewer1"]
        r2 = row["reviewer2"]
        det = row["detector"]
        if not r1.get("present") or not r2.get("present") or not det.get("present"):
            continue
        if not r1.get("canonical") or not r2.get("canonical") or not det.get("canonical"):
            continue

        labels = [r1["canonical"], r2["canonical"], det["canonical"]]
        unique_count = len(set(labels))
        category = triad_category(row)
        category_counts[category] += 1
        if unique_count == 1:
            unanimous += 1
        elif unique_count == 2:
            majority += 1
        else:
            all_different += 1

        if all(label != "unknown" for label in labels):
            known_n += 1
            if unique_count == 1:
                exact_known += 1
        if all(label != "unknown" and not label.startswith("other") for label in labels):
            determinate_n += 1
            if unique_count == 1:
                exact_determinate += 1

        compared.append(
            {
                "sample_id": row["sample_id"],
                "sample_index": row["sample_index"],
                "source": row["source"],
                "model_id": row["model_id"],
                "task_id": row["task_id"],
                "scenario_id": row["scenario_id"],
                "modality": row["modality"],
                "component_file": row["component_file"],
                "component_group": row["component_group"],
                "detector_source_path": row["detector_source_path"],
                "reviewer1_display": r1["display"],
                "reviewer2_display": r2["display"],
                "detector_display": det["display"],
                "reviewer1_canonical": r1["canonical"],
                "reviewer2_canonical": r2["canonical"],
                "detector_canonical": det["canonical"],
                "reviewer1_notes": r1.get("notes", ""),
                "reviewer2_notes": r2.get("notes", ""),
                "detector_provider": det.get("provider", ""),
                "detector_service": det.get("service", ""),
                "detector_confidence": det.get("confidence", ""),
                "triad_category": category,
                "triad_bucket_display": triad_category_label(category),
                "match": unique_count == 1,
            }
        )

    compared_n = len(compared)
    exact_agreement = unanimous / compared_n if compared_n else None
    agreement_known = exact_known / known_n if known_n else None
    agreement_determinate = exact_determinate / determinate_n if determinate_n else None
    majority_rate = majority / compared_n if compared_n else None
    all_different_rate = all_different / compared_n if compared_n else None

    disagreements = [row for row in compared if not row["match"]]
    bucket_rows = [
        {"bucket_display": triad_category_label(category), "category": category, "count": count}
        for category, count in category_counts.items()
        if category != "unanimous"
    ]
    bucket_rows.sort(key=lambda item: (-item["count"], item["bucket_display"]))

    return {
        "compared_count": compared_n,
        "exact_matches": unanimous,
        "exact_agreement": exact_agreement,
        "agreement_excluding_unknown": agreement_known,
        "agreement_determinate_only": agreement_determinate,
        "cohen_kappa": None,
        "unanimous_count": unanimous,
        "unanimous_agreement": exact_agreement,
        "majority_two_of_three_count": majority,
        "majority_two_of_three": majority_rate,
        "all_different_count": all_different,
        "all_different_rate": all_different_rate,
        "category_counts": dict(category_counts),
        "disagreement_buckets": bucket_rows,
        "disagreements": disagreements,
    }


def write_tsv(path: Path, header: list[str], rows: list[list[Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write("\t".join(header) + "\n")
        for row in rows:
            handle.write("\t".join(str(item).replace("\t", " ").replace("\n", " ").strip() for item in row) + "\n")


def render_html(data: dict[str, Any]) -> str:
    payload = json.dumps(data, ensure_ascii=False).replace("</script>", "<\\/script>")
    template = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>VIBench Validation Comparison</title>
  <style>
    :root {{
      --bg: #0b1020;
      --panel: #121a2b;
      --panel-2: #182338;
      --text: #e8edf7;
      --muted: #9fb0cc;
      --border: #253455;
      --accent: #6ea8fe;
      --accent-2: #8ef0c2;
      --warn: #ffd166;
      --bad: #ff7b7b;
      --good: #79e2a0;
      --mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      --sans: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: linear-gradient(180deg, #0b1020 0%, #0d1326 100%);
      color: var(--text);
      font-family: var(--sans);
    }}
    .wrap {{ max-width: 1480px; margin: 0 auto; padding: 24px; }}
    h1, h2, h3 {{ margin: 0; }}
    .muted {{ color: var(--muted); }}
    .header {{
      display: flex;
      justify-content: space-between;
      gap: 16px;
      align-items: end;
      margin-bottom: 20px;
    }}
    .card {{
      background: rgba(18, 26, 43, 0.92);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 16px;
      box-shadow: 0 8px 30px rgba(0,0,0,0.22);
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
      margin-bottom: 16px;
    }}
    .metric {{
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}
    .metric .k {{
      font-size: 12px;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }}
    .metric .v {{
      font-size: 28px;
      font-weight: 700;
    }}
    .metric small {{ color: var(--muted); }}
    .pair-tabs {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 16px;
    }}
    .pair-tab {{
      background: var(--panel-2);
      border: 1px solid var(--border);
      color: var(--text);
      border-radius: 999px;
      padding: 10px 14px;
      cursor: pointer;
      font-weight: 600;
    }}
    .pair-tab.active {{
      border-color: var(--accent);
      background: rgba(110, 168, 254, 0.16);
      color: #dbe9ff;
    }}
    .filters {{
      display: grid;
      grid-template-columns: 1.2fr 1fr 1fr 1fr 2fr;
      gap: 10px;
      margin-bottom: 14px;
    }}
    .filters input, .filters select {{
      width: 100%;
      background: #0d1628;
      color: var(--text);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 10px 12px;
      font: inherit;
    }}
    .section-title {{
      font-size: 14px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--muted);
      margin-bottom: 10px;
    }}
    .two-col {{
      display: grid;
      grid-template-columns: 1.15fr 2fr;
      gap: 16px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
    }}
    th, td {{
      padding: 8px 10px;
      border-bottom: 1px solid rgba(37, 52, 85, 0.9);
      vertical-align: top;
    }}
    th {{
      text-align: left;
      color: var(--muted);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.06em;
    }}
    tr:hover td {{ background: rgba(255,255,255,0.025); }}
    .badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      border-radius: 999px;
      padding: 3px 8px;
      font-size: 12px;
      border: 1px solid var(--border);
      background: rgba(255,255,255,0.03);
      white-space: nowrap;
    }}
    .badge.good {{ color: var(--good); border-color: rgba(121,226,160,0.3); background: rgba(121,226,160,0.08); }}
    .badge.bad {{ color: var(--bad); border-color: rgba(255,123,123,0.3); background: rgba(255,123,123,0.08); }}
    .mono {{ font-family: var(--mono); font-size: 12px; }}
    .pill-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 10px;
    }}
    .pill {{
      display: inline-flex;
      gap: 8px;
      align-items: center;
      background: rgba(255,255,255,0.03);
      border: 1px solid var(--border);
      border-radius: 999px;
      padding: 5px 10px;
      font-size: 12px;
    }}
    .detail {{
      min-height: 220px;
      white-space: pre-wrap;
      word-break: break-word;
    }}
    .empty {{ color: var(--muted); padding: 20px 0; }}
    @media (max-width: 1100px) {{
      .grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      .filters {{ grid-template-columns: 1fr 1fr; }}
      .two-col {{ grid-template-columns: 1fr; }}
    }}
    @media (max-width: 700px) {{
      .grid {{ grid-template-columns: 1fr; }}
      .filters {{ grid-template-columns: 1fr; }}
      .header {{ flex-direction: column; align-items: stretch; }}
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="header">
      <div>
        <h1>VIBench Validation Comparison</h1>
        <div class="muted">Reviewer1, Reviewer2, and current detector alignment on the shared audit sample.</div>
      </div>
      <div class="card">
        <div><strong>Sample-set status</strong></div>
        <div class="muted" id="sample-set-status"></div>
      </div>
    </div>

    <div class="card" style="margin-bottom:16px;">
      <div class="section-title">Global Summary</div>
      <div class="grid" id="global-metrics"></div>
      <div class="pill-row" id="global-pills"></div>
    </div>

    <div class="pair-tabs" id="pair-tabs"></div>

    <div class="card" style="margin-bottom:16px;">
      <div class="section-title">Selected Pair Metrics</div>
      <div class="grid" id="pair-metrics"></div>
    </div>

    <div class="filters">
      <select id="filter-scenario"><option value="">All scenarios</option></select>
      <select id="filter-source"><option value="">All sources</option></select>
      <select id="filter-model"><option value="">All models</option></select>
      <select id="filter-bucket"><option value="">All disagreement buckets</option></select>
      <input id="filter-search" placeholder="Search task, file, labels, notes, detector service..." />
    </div>

    <div class="two-col">
      <div class="card">
        <div class="section-title">Disagreement Buckets</div>
        <div id="bucket-table"></div>
      </div>
      <div class="card">
        <div class="section-title">Disagreements</div>
        <div id="disagreement-table"></div>
      </div>
    </div>

    <div class="card" style="margin-top:16px;">
      <div class="section-title">Selected Case</div>
      <div id="case-detail" class="detail empty">Select a disagreement row.</div>
    </div>
  </div>
  <script>
  const REPORT_DATA = __PAYLOAD__;

  const PAIRS = REPORT_DATA.pair_metrics;
  let activePair = Object.keys(PAIRS)[0];
  let selectedSampleId = null;

  function fmtPct(x) {{
    return x == null ? "N/A" : (x * 100).toFixed(1) + "%";
  }}
  function fmtNum(x, digits = 3) {{
    return x == null ? "N/A" : Number(x).toFixed(digits);
  }}
  function esc(s) {{
    return String(s ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }}
  function pairLabel(key) {{
    const info = REPORT_DATA.pair_labels[key];
    return info ? info.title : key;
  }}
  function pairMeta(key) {{
    return REPORT_DATA.pair_labels[key] || {{ mode: "pair", left: "reviewer1", right: "reviewer2" }};
  }}
  function activeRows() {{
    return PAIRS[activePair].disagreements || [];
  }}
  function activeBuckets() {{
    return PAIRS[activePair].disagreement_buckets || [];
  }}
  function buildGlobal() {{
    const meta = REPORT_DATA.meta;
    document.getElementById("sample-set-status").textContent =
      meta.same_sample_set
        ? `Both reviewers covered the same ${meta.shared_sample_id_count} sample IDs.`
        : `Reviewer overlap: ${meta.shared_sample_id_count} shared IDs; sets differ.`;

    const global = [
      ["Reviewer1 rows", meta.reviewer1_row_count],
      ["Reviewer2 rows", meta.reviewer2_row_count],
      ["Shared sample IDs", meta.shared_sample_id_count],
      ["Current detector rows", meta.detector_row_count],
    ];
    document.getElementById("global-metrics").innerHTML = global.map(([k, v]) => `
      <div class="metric">
        <div class="k">${{esc(k)}}</div>
        <div class="v">${{esc(v)}}</div>
      </div>`).join("");
    document.getElementById("global-pills").innerHTML = [
      `Reviewer1 file: ${{esc(meta.reviewer1_csv)}}`,
      `Reviewer2 file: ${{esc(meta.reviewer2_csv)}}`,
      `Generated: ${{esc(meta.generated_at_utc)}} UTC`,
    ].map(text => `<div class="pill">${{text}}</div>`).join("");
  }}
  function buildPairTabs() {{
    const keys = Object.keys(PAIRS);
    document.getElementById("pair-tabs").innerHTML = keys.map(key => `
      <button class="pair-tab ${{key === activePair ? "active" : ""}}" data-pair="${{esc(key)}}">${{esc(pairLabel(key))}}</button>
    `).join("");
    document.querySelectorAll(".pair-tab").forEach(btn => {{
      btn.addEventListener("click", () => {{
        activePair = btn.dataset.pair;
        selectedSampleId = null;
        render();
      }});
    }});
  }}
  function buildPairMetrics() {{
    const data = PAIRS[activePair];
    const metrics = pairMeta(activePair).mode === "triad"
      ? [
          ["Compared rows", data.compared_count],
          ["All three agree", fmtPct(data.unanimous_agreement ?? data.exact_agreement)],
          ["Two of three agree", fmtPct(data.majority_two_of_three)],
          ["All three differ", fmtPct(data.all_different_rate)],
          ["Agreement excl. unknown", fmtPct(data.agreement_excluding_unknown)],
          ["Disagreements", (data.disagreements || []).length],
        ]
      : [
          ["Compared rows", data.compared_count],
          ["Exact agreement", fmtPct(data.exact_agreement)],
          ["Agreement excl. unknown", fmtPct(data.agreement_excluding_unknown)],
          ["Agreement determinate only", fmtPct(data.agreement_determinate_only)],
          ["Cohen’s kappa", fmtNum(data.cohen_kappa)],
          ["Disagreements", (data.disagreements || []).length],
        ];
    document.getElementById("pair-metrics").innerHTML = metrics.map(([k, v]) => `
      <div class="metric">
        <div class="k">${{esc(k)}}</div>
        <div class="v">${{esc(v)}}</div>
      </div>`).join("");
  }}
  function ensureFilters() {{
    const rows = activeRows();
    const setOptions = (id, values, labeler) => {{
      const el = document.getElementById(id);
      const current = el.value;
      el.innerHTML = `<option value="">${{labeler}}</option>` + values.map(v => `<option value="${{esc(v)}}">${{esc(v)}}</option>`).join("");
      if (values.includes(current)) el.value = current;
    }};
    setOptions("filter-scenario", [...new Set(rows.map(r => r.scenario_id).filter(Boolean))].sort(), "All scenarios");
    setOptions("filter-source", [...new Set(rows.map(r => r.source).filter(Boolean))].sort(), "All sources");
    setOptions("filter-model", [...new Set(rows.map(r => r.model_id).filter(Boolean))].sort(), "All models");
    setOptions(
      "filter-bucket",
      activeBuckets().map(b => pairMeta(activePair).mode === "triad"
        ? (b.category || b.bucket_display)
        : `${{b.left_display}}|||${{b.right_display}}`
      ),
      "All disagreement buckets"
    );
  }}
  function filteredRows() {{
    const scenario = document.getElementById("filter-scenario").value;
    const source = document.getElementById("filter-source").value;
    const model = document.getElementById("filter-model").value;
    const bucket = document.getElementById("filter-bucket").value;
    const search = document.getElementById("filter-search").value.trim().toLowerCase();
    const triad = pairMeta(activePair).mode === "triad";
    return activeRows().filter(row => {{
      if (scenario && row.scenario_id !== scenario) return false;
      if (source && row.source !== source) return false;
      if (model && row.model_id !== model) return false;
      if (bucket) {{
        const bucketKey = triad ? (row.triad_category || "") : `${{row.left_display}}|||${{row.right_display}}`;
        if (bucketKey !== bucket) return false;
      }}
      if (!search) return true;
      const hay = [
        row.task_id, row.component_file, row.left_display, row.right_display,
        row.left_notes, row.right_notes, row.right_provider, row.right_service,
        row.reviewer1_display, row.reviewer2_display, row.detector_display, row.triad_bucket_display,
        row.modality, row.model_id, row.detector_source_path,
      ].join(" ").toLowerCase();
      return hay.includes(search);
    }});
  }}
  function buildBucketTable() {{
    const rows = activeBuckets();
    const triad = pairMeta(activePair).mode === "triad";
    document.getElementById("bucket-table").innerHTML = rows.length ? (
      triad
        ? `<table>
            <thead><tr><th>Bucket</th><th>Count</th></tr></thead>
            <tbody>
              ${rows.map(r => `<tr><td>${esc(r.bucket_display)}</td><td>${r.count}</td></tr>`).join("")}
            </tbody>
          </table>`
        : `<table>
            <thead><tr><th>Left</th><th>Right</th><th>Count</th></tr></thead>
            <tbody>
              ${rows.map(r => `<tr><td>${esc(r.left_display)}</td><td>${esc(r.right_display)}</td><td>${r.count}</td></tr>`).join("")}
            </tbody>
          </table>`
    ) : `<div class="empty">No disagreements.</div>`;
  }}
  function buildDisagreementTable() {{
    const rows = filteredRows();
    const triad = pairMeta(activePair).mode === "triad";
    document.getElementById("disagreement-table").innerHTML = rows.length ? (
      triad
        ? `<table>
            <thead><tr><th>#</th><th>Scenario</th><th>Model</th><th>File</th><th>Reviewer1</th><th>Reviewer2</th><th>Detector</th></tr></thead>
            <tbody>
              ${rows.map(r => `<tr data-sid="${esc(r.sample_id)}">
                <td class="mono">${r.sample_index + 1}</td>
                <td>${esc(r.scenario_id || r.task_id)}</td>
                <td>${esc(r.model_id)}</td>
                <td class="mono">${esc(r.component_file || "-")}</td>
                <td><span class="badge bad">${esc(r.reviewer1_display)}</span></td>
                <td><span class="badge bad">${esc(r.reviewer2_display)}</span></td>
                <td><span class="badge ${r.detector_provider ? "good" : "bad"}">${esc(r.detector_display)}</span></td>
              </tr>`).join("")}
            </tbody>
          </table>`
        : `<table>
            <thead><tr><th>#</th><th>Scenario</th><th>Model</th><th>File</th><th>Left</th><th>Right</th></tr></thead>
            <tbody>
              ${rows.map(r => `<tr data-sid="${esc(r.sample_id)}">
                <td class="mono">${r.sample_index + 1}</td>
                <td>${esc(r.scenario_id || r.task_id)}</td>
                <td>${esc(r.model_id)}</td>
                <td class="mono">${esc(r.component_file || "-")}</td>
                <td><span class="badge bad">${esc(r.left_display)}</span></td>
                <td><span class="badge ${r.right_provider ? "good" : "bad"}">${esc(r.right_display)}</span></td>
              </tr>`).join("")}
            </tbody>
          </table>`
    ) : `<div class="empty">No disagreements match the current filters.</div>`;
    document.querySelectorAll("#disagreement-table tr[data-sid]").forEach(tr => {{
      tr.addEventListener("click", () => {{
        selectedSampleId = tr.dataset.sid;
        buildCaseDetail();
      }});
    }});
  }}
  function buildCaseDetail() {{
    const rows = activeRows();
    const row = rows.find(r => r.sample_id === selectedSampleId) || rows[0];
    const triad = pairMeta(activePair).mode === "triad";
    if (!row) {{
      document.getElementById("case-detail").innerHTML = `<div class="empty">Select a disagreement row.</div>`;
      return;
    }}
    selectedSampleId = row.sample_id;
    document.getElementById("case-detail").innerHTML = `
      <div class="pill-row" style="margin-bottom:12px;">
        <div class="pill">sample <span class="mono">${esc(row.sample_id)}</span></div>
        <div class="pill">${esc(row.source)} · ${esc(row.modality)}</div>
        <div class="pill">${esc(row.scenario_id || row.task_id)}</div>
        <div class="pill">${esc(row.model_id)}</div>
      </div>
      <table>
        <tbody>
          <tr><th style="width:180px;">Task</th><td class="mono">${esc(row.task_id)}</td></tr>
          <tr><th>Component</th><td class="mono">${esc(row.component_file || "-")}</td></tr>
          ${triad
            ? `<tr><th>Reviewer1</th><td>${esc(row.reviewer1_display)}</td></tr>
               <tr><th>Reviewer2</th><td>${esc(row.reviewer2_display)}</td></tr>
               <tr><th>Detector</th><td>${esc(row.detector_display)}</td></tr>
               <tr><th>Bucket</th><td>${esc(row.triad_bucket_display)}</td></tr>`
            : `<tr><th>Left label</th><td>${esc(row.left_display)}</td></tr>
               <tr><th>Right label</th><td>${esc(row.right_display)}</td></tr>`}
          <tr><th>Right provider</th><td>${esc(row.right_provider || "-")}</td></tr>
          <tr><th>Right service</th><td>${esc(row.right_service || "-")}</td></tr>
          <tr><th>Right confidence</th><td>${esc(row.right_confidence || "-")}</td></tr>
          <tr><th>Source path</th><td class="mono">${esc(row.detector_source_path || "-")}</td></tr>
          ${triad
            ? `<tr><th>Reviewer1 notes</th><td>${esc(row.reviewer1_notes || "-")}</td></tr>
               <tr><th>Reviewer2 notes</th><td>${esc(row.reviewer2_notes || "-")}</td></tr>`
            : `<tr><th>Left notes</th><td>${esc(row.left_notes || "-")}</td></tr>
               <tr><th>Right notes</th><td>${esc(row.right_notes || "-")}</td></tr>`}
        </tbody>
      </table>`;
  }}
  function render() {{
    buildPairTabs();
    buildPairMetrics();
    ensureFilters();
    buildBucketTable();
    buildDisagreementTable();
    buildCaseDetail();
  }}
  ["filter-scenario","filter-source","filter-model","filter-bucket","filter-search"].forEach(id => {{
    document.addEventListener("input", e => {{
      if (e.target && e.target.id === id) {{
        buildDisagreementTable();
        buildCaseDetail();
      }}
    }});
    document.addEventListener("change", e => {{
      if (e.target && e.target.id === id) {{
        buildDisagreementTable();
        buildCaseDetail();
      }}
    }});
  }});
  buildGlobal();
  render();
  </script>
</body>
</html>"""
    template = template.replace("{{", "{").replace("}}", "}")
    return template.replace("__PAYLOAD__", payload)


def build_report(
    reviewer1_csv: Path,
    reviewer2_csv: Path,
    out_dir: Path,
) -> dict[str, Any]:
    reviewer1_rows = load_csv_rows(reviewer1_csv)
    reviewer2_rows = load_csv_rows(reviewer2_csv)

    reviewer1_by_id = {normalize_text(row.get("sample_id")): row for row in reviewer1_rows if normalize_text(row.get("sample_id"))}
    reviewer2_by_id = {normalize_text(row.get("sample_id")): row for row in reviewer2_rows if normalize_text(row.get("sample_id"))}

    reviewer1_ids = list(reviewer1_by_id)
    reviewer2_ids = list(reviewer2_by_id)
    shared_ids = set(reviewer1_by_id) & set(reviewer2_by_id)
    all_ids = set(reviewer1_by_id) | set(reviewer2_by_id)
    order_ids = reviewer2_ids + [sample_id for sample_id in reviewer1_ids if sample_id not in reviewer2_by_id]

    detector_by_id = build_detector_rows(all_ids)

    combined_rows: list[dict[str, Any]] = []
    for sample_index, sample_id in enumerate(order_ids):
        r1 = reviewer1_by_id.get(sample_id)
        r2 = reviewer2_by_id.get(sample_id)
        detector_row = detector_by_id.get(sample_id)
        meta = row_metadata(detector_row, r2 or r1)
        combined_rows.append(
            {
                "sample_id": sample_id,
                "sample_index": sample_index,
                **meta,
                "reviewer1": reviewer_record(r1) if r1 else {"present": False, "label": "", "other_label": "", "notes": "", "canonical": "", "display": ""},
                "reviewer2": reviewer_record(r2) if r2 else {"present": False, "label": "", "other_label": "", "notes": "", "canonical": "", "display": ""},
                "detector": detector_record(detector_row),
            }
        )

    # Text extracts
    txt_dir = out_dir / "txt"
    write_tsv(
        txt_dir / "reviewer1_choices.txt",
        ["sample_index", "sample_id", "source", "model_id", "task_id", "scenario_id", "modality", "component_file", "human_label", "human_display", "human_other_label", "notes"],
        [
            [
                row["sample_index"],
                row["sample_id"],
                row["source"],
                row["model_id"],
                row["task_id"],
                row["scenario_id"],
                row["modality"],
                row["component_file"],
                row["reviewer1"]["label"],
                row["reviewer1"]["display"],
                row["reviewer1"]["other_label"],
                row["reviewer1"]["notes"],
            ]
            for row in combined_rows
        ],
    )
    write_tsv(
        txt_dir / "reviewer2_choices.txt",
        ["sample_index", "sample_id", "source", "model_id", "task_id", "scenario_id", "modality", "component_file", "human_label", "human_display", "human_other_label", "notes"],
        [
            [
                row["sample_index"],
                row["sample_id"],
                row["source"],
                row["model_id"],
                row["task_id"],
                row["scenario_id"],
                row["modality"],
                row["component_file"],
                row["reviewer2"]["label"],
                row["reviewer2"]["display"],
                row["reviewer2"]["other_label"],
                row["reviewer2"]["notes"],
            ]
            for row in combined_rows
        ],
    )
    write_tsv(
        txt_dir / "detector_choices.txt",
        ["sample_index", "sample_id", "source", "model_id", "task_id", "scenario_id", "modality", "component_file", "detector_ecosystem", "detector_provider", "detector_service", "detector_confidence", "source_path"],
        [
            [
                row["sample_index"],
                row["sample_id"],
                row["source"],
                row["model_id"],
                row["task_id"],
                row["scenario_id"],
                row["modality"],
                row["component_file"],
                row["detector"]["display"],
                row["detector"]["provider"],
                row["detector"]["service"],
                row["detector"]["confidence"],
                row["detector"]["source_path"],
            ]
            for row in combined_rows
        ],
    )

    pairs = {
        "reviewer1_vs_reviewer2": pair_metrics(combined_rows, "reviewer1", "reviewer2"),
        "reviewer1_vs_detector": pair_metrics(combined_rows, "reviewer1", "detector"),
        "reviewer2_vs_detector": pair_metrics(combined_rows, "reviewer2", "detector"),
        "reviewer1_vs_reviewer2_vs_detector": triad_metrics(combined_rows),
    }
    pair_labels = {
        "reviewer1_vs_reviewer2": {"title": "Reviewer1 vs Reviewer2", "mode": "pair", "left": "reviewer1", "right": "reviewer2"},
        "reviewer1_vs_detector": {"title": "Reviewer1 vs Current Detector", "mode": "pair", "left": "reviewer1", "right": "detector"},
        "reviewer2_vs_detector": {"title": "Reviewer2 vs Current Detector", "mode": "pair", "left": "reviewer2", "right": "detector"},
        "reviewer1_vs_reviewer2_vs_detector": {"title": "Reviewer1 vs Reviewer2 vs Detector", "mode": "triad"},
    }

    report = {
        "meta": {
            "reviewer1_csv": display_path(reviewer1_csv),
            "reviewer2_csv": display_path(reviewer2_csv),
            "reviewer1_row_count": len(reviewer1_rows),
            "reviewer2_row_count": len(reviewer2_rows),
            "shared_sample_id_count": len(shared_ids),
            "reviewer1_only_sample_id_count": len(set(reviewer1_by_id) - shared_ids),
            "reviewer2_only_sample_id_count": len(set(reviewer2_by_id) - shared_ids),
            "same_sample_set": set(reviewer1_by_id) == set(reviewer2_by_id),
            "detector_row_count": len(detector_by_id),
            "generated_at_utc": datetime.utcnow().replace(microsecond=0).isoformat(),
        },
        "pair_labels": pair_labels,
        "pair_metrics": pairs,
        "rows": combined_rows,
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "alignment_data.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    summary = {
        "meta": report["meta"],
        "pair_metrics": {
            key: {
                "compared_count": value["compared_count"],
                "exact_matches": value["exact_matches"],
                "exact_agreement": value["exact_agreement"],
                "agreement_excluding_unknown": value["agreement_excluding_unknown"],
                "agreement_determinate_only": value["agreement_determinate_only"],
                "cohen_kappa": value["cohen_kappa"],
                "disagreement_count": len(value["disagreements"]),
                "majority_two_of_three": value.get("majority_two_of_three"),
                "all_different_rate": value.get("all_different_rate"),
            }
            for key, value in pairs.items()
        },
    }
    (out_dir / "alignment_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Build reviewer/detector alignment extracts and static report.")
    parser.add_argument("--reviewer1", type=Path, default=VALIDATION_DIR / "reviewer1.csv")
    parser.add_argument("--reviewer2", type=Path, default=VALIDATION_DIR / "reviewer2.csv")
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    args = parser.parse_args()

    summary = build_report(args.reviewer1, args.reviewer2, args.out_dir)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
