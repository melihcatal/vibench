import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


def _get_client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def _extract_records(payload: Any) -> List[Dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if isinstance(payload, dict):
        for key in ("results", "data", "jobs", "items", "records"):
            value = payload.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
    return []


def _record_text(record: Dict[str, Any]) -> str:
    parts = []
    for key in ("id", "status", "embedding_model", "model", "dimensions", "count", "processed", "failed", "duration_seconds", "error"):
        if key in record and record[key] is not None:
            parts.append(f"{key}={record[key]}")
    if not parts:
        parts.append(str(record))
    return "; ".join(parts)


def summarize_embedding_jobs(payload: Any, model: str = "gpt-5.4-mini") -> str:
    records = _extract_records(payload)
    total = len(records)
    status_counts: Dict[str, int] = {}
    failed = 0
    processed = 0
    for record in records:
        status = str(record.get("status", "unknown"))
        status_counts[status] = status_counts.get(status, 0) + 1
        failed += int(record.get("failed") or 0)
        processed += int(record.get("processed") or record.get("count") or 0)

    job_lines = [f"Total jobs: {total}", f"Processed items: {processed}", f"Failed items: {failed}"]
    if status_counts:
        job_lines.append("Status counts: " + ", ".join(f"{k}={v}" for k, v in sorted(status_counts.items())))
    if records:
        job_lines.append("Job details:")
        job_lines.extend(f"- {_record_text(record)}" for record in records[:20])

    prompt = "\n".join(job_lines)
    client = _get_client()
    response = client.responses.create(
        model=model,
        input=(
            "Summarize these embedding job results concisely, highlighting throughput, failures, and any notable patterns:\n"
            + prompt
        ),
    )
    return response.output_text


def main() -> None:
    import json
    import sys

    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            payload = json.load(f)
    else:
        payload = json.load(sys.stdin)
    print(summarize_embedding_jobs(payload))


if __name__ == "__main__":
    main()
