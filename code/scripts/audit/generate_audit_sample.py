#!/usr/bin/env python3
"""Generate a seeded human-audit sample from current VIBench outputs.

The JSONL output is the seeded detector-audit sample used for reviewer
agreement checks. Detector labels are included in each row for downstream
agreement computation.

Examples:
    python scripts/audit/generate_audit_sample.py

    python scripts/audit/generate_audit_sample.py \
        --n 400 --seed 42 \
        --out benchmark/vibench/audit/vibench_detector_audit.jsonl

    python scripts/audit/generate_audit_sample.py \
        --run direct/complete/full_5c \
        --run agentic/complete/opencode_full_5c
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from collections import Counter, defaultdict
from pathlib import Path

# The corpus lives under code/; the generated runs sit beside it at the
# repository root, and sample source_paths are recorded relative to that root.
REPO = Path(__file__).resolve().parents[2]
REPO_ROOT = REPO.parent
RUNS_ROOT = REPO_ROOT / "outputs" / "runs"
DEFAULT_OUT = REPO / "benchmark" / "vibench" / "audit" / "vibench_detector_audit.jsonl"

MAX_OUTPUT = 3000
MAX_SIBLING = 2000


def _truncate(text: str, limit: int) -> str:
    if not text:
        return ""
    return text if len(text) <= limit else text[:limit] + "\n... [truncated]"


def _resolve_run(value: str) -> Path:
    path = Path(value)
    if path.is_dir():
        return path
    candidate = RUNS_ROOT / value
    if candidate.is_dir():
        return candidate
    matches = [
        p
        for p in _discover_current_runs()
        if value in p.name or value in _run_id(p)
    ]
    if matches:
        return sorted(matches)[-1]
    raise SystemExit(f"Run not found: {value}")


def _discover_current_runs() -> list[Path]:
    if not RUNS_ROOT.is_dir():
        return []
    return sorted({p.parent for p in RUNS_ROOT.rglob("labeled") if p.is_dir()})


def _run_id(run: Path) -> str:
    try:
        return run.resolve().relative_to(RUNS_ROOT.resolve()).as_posix()
    except ValueError:
        return run.name


def _source_path(path: Path | None) -> str:
    if path is None:
        return ""
    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def load_direct_pool(run: Path) -> list[dict]:
    pool = []
    labeled = run / "labeled"
    for modality in ["nli", "fim", "reference_open"]:
        mod_dir = labeled / modality
        if not mod_dir.is_dir():
            continue
        for model_dir in sorted(mod_dir.iterdir()):
            if not model_dir.is_dir():
                continue
            for json_file in sorted(model_dir.glob("*.json")):
                try:
                    rec = json.loads(json_file.read_text(encoding="utf-8"))
                except (json.JSONDecodeError, OSError):
                    continue
                output_text = _truncate(rec.get("output_text") or "", MAX_OUTPUT)
                if not output_text.strip():
                    continue
                pool.append({
                    "source": "direct",
                    "run_id": _run_id(run),
                    "source_path": _source_path(json_file),
                    "model_id": rec.get("model_id", ""),
                    "task_id": rec.get("task_id", ""),
                    "modality": rec.get("modality", modality),
                    "scenario_id": rec.get("scenario_id", ""),
                    "output_text": output_text,
                    "detector_provider": rec.get("detected_provider", ""),
                    "detector_ecosystem": rec.get("detected_ecosystem", ""),
                    "detector_service": rec.get("detected_service", ""),
                    "detector_confidence": rec.get("detection_confidence", ""),
                    "detector_method": rec.get("detection_method", ""),
                })
    return pool


def load_agentic_pool(run: Path, include_unscored: bool) -> list[dict]:
    pool = []
    results_file = run / "labeled" / "agentic" / "results.json"
    if not results_file.exists():
        return pool
    try:
        records = json.loads(results_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return pool
    if not isinstance(records, list):
        return pool

    raw_root = run / "raw" / "agentic"
    for arec in records:
        model_id = arec.get("model_id", "")
        task_id = arec.get("task_id", "")
        variant = arec.get("variant", "")
        completion_index = arec.get("completion_index", 1)
        session_key = f"{task_id}__{variant}__c{completion_index}"
        session_dir = raw_root / model_id / session_key
        sibling_cache = None

        components = arec.get("components", {})
        if not isinstance(components, dict):
            continue

        for component_key, component in components.items():
            if not include_unscored and not component.get("is_scored"):
                continue
            file_name = component.get("file", "")
            file_path = session_dir / file_name if file_name else None
            content = ""
            if file_path and file_path.exists():
                try:
                    content = _truncate(file_path.read_text(encoding="utf-8"), MAX_OUTPUT)
                except OSError:
                    content = ""
            if not content.strip():
                continue

            if sibling_cache is None:
                sibling_cache = {}
                if session_dir.is_dir():
                    for sibling in sorted(session_dir.glob("*.py")):
                        try:
                            sibling_cache[sibling.name] = _truncate(
                                sibling.read_text(encoding="utf-8"),
                                MAX_SIBLING,
                            )
                        except OSError:
                            continue

            pool.append({
                "source": "agentic",
                "run_id": _run_id(run),
                "source_path": _source_path(file_path),
                "model_id": model_id,
                "task_id": task_id,
                "modality": f"agentic_{variant}",
                "variant": variant,
                "scenario_id": arec.get("primary_atomic_scenario", ""),
                "component_key": component_key,
                "component_file": file_name,
                "component_group": component.get("component_group", ""),
                "component_role": component.get("role", component_key),
                "coupling_expectation": component.get("coupling_expectation", ""),
                "is_scored": bool(component.get("is_scored")),
                "output_text": content,
                "detector_provider": component.get("provider", ""),
                "detector_ecosystem": component.get("ecosystem", ""),
                "detector_service": component.get("service", ""),
                "detector_confidence": component.get("confidence", ""),
                "detector_method": "",
                "sibling_files": {
                    name: value
                    for name, value in (sibling_cache or {}).items()
                    if name != file_name
                },
            })
    return pool


# The config-variant runs moved from outputs/runs/<mode>/ablations/ to
# <mode>/variants/. Both the sample ordering and the sample id are derived from
# the run path, and the shipped n=400 sample plus both reviewer CSVs key off
# those ids, so the identity fields are canonicalised to the original spelling.
# The record itself keeps the current path; only identity is pinned.
_CANONICAL_RUN_SEGMENTS = [("/variants/", "/ablations/")]


def _canonical_identity(record: dict) -> list:
    run_id = record.get("run_id") or ""
    source_path = record.get("source_path") or ""
    for current, legacy in _CANONICAL_RUN_SEGMENTS:
        run_id = run_id.replace(current.strip("/"), legacy.strip("/"))
        source_path = source_path.replace(current, legacy)
    return [
        run_id,
        record.get("source") or "",
        record.get("model_id") or "",
        record.get("task_id") or "",
        record.get("modality") or "",
        record.get("component_file") or "",
        source_path,
    ]


def _sort_key(record: dict) -> tuple:
    return tuple(_canonical_identity(record))


def _sample_random(pool: list[dict], n: int, rng: random.Random) -> list[dict]:
    pool = sorted(pool, key=_sort_key)
    if len(pool) <= n:
        return pool[:]
    return rng.sample(pool, n)


def _sample_stratified(pool: list[dict], n: int, rng: random.Random) -> list[dict]:
    by_stratum = defaultdict(list)
    for item in pool:
        by_stratum[(item["source"], item.get("modality", ""), item.get("detector_ecosystem", "unknown"))].append(item)
    strata = sorted(by_stratum)
    if not strata:
        return []

    picked = []
    base = max(1, n // len(strata))
    for stratum in strata:
        items = sorted(by_stratum[stratum], key=_sort_key)
        take = min(base, len(items))
        picked.extend(rng.sample(items, take))

    picked_ids = {id(item) for item in picked}
    remaining = [item for item in pool if id(item) not in picked_ids]
    if len(picked) < n:
        picked.extend(rng.sample(remaining, min(n - len(picked), len(remaining))))
    elif len(picked) > n:
        picked = rng.sample(picked, n)
    return picked


def _expand_filter_values(values: list[str]) -> list[str]:
    items: list[str] = []
    for value in values:
        for piece in value.split(","):
            piece = piece.strip()
            if piece:
                items.append(piece)
    return items


def _filter_pool(
    pool: list[dict],
    *,
    scenarios: list[str] | None = None,
    models: list[str] | None = None,
    run_ids: list[str] | None = None,
) -> list[dict]:
    scenario_set = set(scenarios or [])
    model_set = set(models or [])
    run_set = set(run_ids or [])
    filtered = []
    for item in pool:
        if scenario_set and item.get("scenario_id") not in scenario_set:
            continue
        if model_set and item.get("model_id") not in model_set:
            continue
        if run_set and item.get("run_id") not in run_set:
            continue
        filtered.append(item)
    return filtered


def assign_sample_ids(samples: list[dict]) -> None:
    seen = set()
    for index, sample in enumerate(samples):
        raw = json.dumps(_canonical_identity(sample), separators=(",", ":"))
        sample_id = hashlib.sha256(raw.encode()).hexdigest()[:12]
        salt = 0
        while sample_id in seen:
            salt += 1
            sample_id = hashlib.sha256((raw + f"#{salt}").encode()).hexdigest()[:12]
        seen.add(sample_id)
        sample["sample_id"] = sample_id
        sample["sample_index"] = index


def summarize(samples: list[dict], pool_size: int, runs: list[Path], seed: int, strategy: str) -> dict:
    by_run = Counter(sample["run_id"] for sample in samples)
    by_source = Counter(sample["source"] for sample in samples)
    by_model = Counter(sample["model_id"] for sample in samples)
    by_modality = Counter(sample["modality"] for sample in samples)
    by_scenario = Counter(sample.get("scenario_id") or "unknown" for sample in samples)
    by_detector = Counter(sample.get("detector_ecosystem") or "unknown" for sample in samples)
    return {
        "seed": seed,
        "strategy": strategy,
        "pool_size": pool_size,
        "sample_size": len(samples),
        "runs": [_run_id(run) for run in runs],
        "by_run": dict(sorted(by_run.items())),
        "by_source": dict(sorted(by_source.items())),
        "by_model": dict(sorted(by_model.items())),
        "by_modality": dict(sorted(by_modality.items())),
        "by_scenario": dict(sorted(by_scenario.items())),
        "by_detector_ecosystem": dict(sorted(by_detector.items())),
    }


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=400)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--run", action="append", default=[], help="Run folder name or path. Defaults to all current labeled runs.")
    parser.add_argument("--scenario", action="append", default=[], help="Scenario ID filter. Repeat or use comma-separated values, e.g. --scenario S19,S20")
    parser.add_argument("--model", action="append", default=[], help="Model ID filter. Repeat or use comma-separated values.")
    parser.add_argument("--run-id", action="append", default=[], help="Filter sampled rows to these resolved run ids. Repeat or use comma-separated values.")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--strategy", choices=["random", "stratified"], default="random")
    parser.add_argument("--include-unscored-agentic", action="store_true")
    parser.add_argument("--summary-out", type=Path)
    parser.add_argument("--key-out", type=Path)
    parser.add_argument("--force", action="store_true",
                        help="Overwrite an existing sample file (see the warning below).")
    args = parser.parse_args()

    # The shipped sample is human-annotated reference data: reviewer1.csv and
    # reviewer2.csv key off its sample ids, and build_alignment_report.py
    # reconstructs those exact 400 rows to produce the reported agreement. A
    # fresh draw is a different 400 rows, so overwriting it silently invalidates
    # the annotations. Refuse unless the caller means it.
    if args.out.exists() and not args.force:
        raise SystemExit(
            f"{args.out} already exists and would be replaced by a different\n"
            f"sample. The reviewer CSVs are keyed to the ids in that file, so\n"
            f"replacing it breaks the annotator-agreement report.\n\n"
            f"  To draw a fresh sample elsewhere:  --out <new path>\n"
            f"  To replace the shipped sample:     --force"
        )

    runs = [_resolve_run(value) for value in args.run] if args.run else _discover_current_runs()
    if not runs:
        raise SystemExit("No labeled VIBench runs found.")

    pool = []
    for run in runs:
        pool.extend(load_direct_pool(run))
        pool.extend(load_agentic_pool(run, include_unscored=args.include_unscored_agentic))
    pool = _filter_pool(
        pool,
        scenarios=_expand_filter_values(args.scenario),
        models=_expand_filter_values(args.model),
        run_ids=_expand_filter_values(args.run_id),
    )
    if len(pool) < args.n:
        raise SystemExit(f"Requested {args.n} samples, but only {len(pool)} records are available.")

    rng = random.Random(args.seed)
    if args.strategy == "stratified":
        samples = _sample_stratified(pool, args.n, rng)
    else:
        samples = _sample_random(pool, args.n, rng)
    rng.shuffle(samples)
    assign_sample_ids(samples)

    write_jsonl(args.out, samples)

    summary = summarize(samples, len(pool), runs, args.seed, args.strategy)
    summary_out = args.summary_out or args.out.with_suffix(".summary.json")
    summary_out.parent.mkdir(parents=True, exist_ok=True)
    summary_out.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    key_out = args.key_out or args.out.with_suffix(".key.jsonl")
    key_rows = [
        {
            "sample_id": sample["sample_id"],
            "sample_index": sample["sample_index"],
            "run_id": sample["run_id"],
            "source": sample["source"],
            "model_id": sample["model_id"],
            "task_id": sample["task_id"],
            "modality": sample["modality"],
            "component_file": sample.get("component_file", ""),
            "detector_provider": sample.get("detector_provider", ""),
            "detector_ecosystem": sample.get("detector_ecosystem", ""),
            "detector_service": sample.get("detector_service", ""),
            "detector_confidence": sample.get("detector_confidence", ""),
        }
        for sample in samples
    ]
    write_jsonl(key_out, key_rows)

    print(json.dumps({"out": str(args.out), "summary": str(summary_out), "key": str(key_out), **summary}, indent=2))


if __name__ == "__main__":
    main()
