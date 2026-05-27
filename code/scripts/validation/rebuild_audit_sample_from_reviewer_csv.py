from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR / "scripts" / "evaluation"))
sys.path.insert(0, str(BASE_DIR / "scripts" / "audit"))

from generate_audit_sample import _discover_current_runs, load_agentic_pool, load_direct_pool  # noqa: E402
from run_vibench_detector_llm_judge import reconstruct_samples_by_id  # noqa: E402


def load_reviewer_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def sample_id_for_pool_row(row: dict) -> str:
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


def build_full_pool() -> list[dict]:
    pool: list[dict] = []
    for run in _discover_current_runs():
        pool.extend(load_direct_pool(run))
        pool.extend(load_agentic_pool(run, include_unscored=False))
    return pool


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Rebuild a canonical audit JSONL from reviewer CSV sample_ids."
    )
    parser.add_argument(
        "--reviewer-csv",
        type=Path,
        required=True,
        help="Reviewer CSV with a sample_id column.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        required=True,
        help="Output JSONL path for the reconstructed audit sample.",
    )
    parser.add_argument(
        "--summary-out",
        type=Path,
        help="Optional summary JSON path.",
    )
    args = parser.parse_args()

    reviewer_rows = load_reviewer_rows(args.reviewer_csv)
    ordered_ids: list[str] = []
    for row in reviewer_rows:
        sample_id = (row.get("sample_id") or "").strip()
        if sample_id:
            ordered_ids.append(sample_id)

    unique_ids = list(dict.fromkeys(ordered_ids))
    full_pool = build_full_pool()
    pool_by_id = {}
    for row in full_pool:
        sample_id = sample_id_for_pool_row(row)
        enriched = dict(row)
        enriched["sample_id"] = sample_id
        pool_by_id[sample_id] = enriched

    missing = [sample_id for sample_id in unique_ids if sample_id not in pool_by_id]
    if missing:
        # Fallback check, mainly to surface whether the IDs came from older audit logic.
        recovered_rows = reconstruct_samples_by_id(set(unique_ids))
        recovered_by_id = {row["sample_id"]: row for row in recovered_rows}
        unresolved = [sample_id for sample_id in unique_ids if sample_id not in recovered_by_id]
        if unresolved:
            raise RuntimeError(
                f"Failed to recover {len(unresolved)} sample ids from current retained runs. "
                f"First missing ids: {unresolved[:10]}"
            )
        raise RuntimeError(
            "Reviewer sample ids were recoverable only through the reduced judge schema, "
            "not the full audit pool schema. This indicates a pool/schema mismatch that should be fixed first."
        )

    ordered_rows = [dict(pool_by_id[sample_id]) for sample_id in ordered_ids]
    for index, row in enumerate(ordered_rows):
        row["sample_index"] = index

    write_jsonl(args.out, ordered_rows)

    if args.summary_out:
        summary = {
            "reviewer_csv": str(args.reviewer_csv),
            "output_jsonl": str(args.out),
            "row_count": len(reviewer_rows),
            "sample_id_count": len(ordered_ids),
            "unique_sample_id_count": len(unique_ids),
            "duplicate_sample_ids": {
                sample_id: count
                for sample_id, count in Counter(ordered_ids).items()
                if count > 1
            },
            "by_source": dict(sorted(Counter(row.get("source", "") for row in ordered_rows).items())),
            "by_modality": dict(sorted(Counter(row.get("modality", "") for row in ordered_rows).items())),
            "by_scenario": dict(
                sorted(Counter(row.get("scenario_id", "") or "unknown" for row in ordered_rows).items())
            ),
        }
        args.summary_out.parent.mkdir(parents=True, exist_ok=True)
        args.summary_out.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(f"Recovered {len(unique_ids)} unique rows from {len(unique_ids)} sample ids.")
    print(f"Wrote {len(ordered_rows)} rows to {args.out}")
    if args.summary_out:
        print(f"Wrote summary to {args.summary_out}")


if __name__ == "__main__":
    main()
