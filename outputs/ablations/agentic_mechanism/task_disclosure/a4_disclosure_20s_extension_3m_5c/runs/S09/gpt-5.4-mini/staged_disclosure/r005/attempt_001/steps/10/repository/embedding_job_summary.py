import json
import os
from typing import Any, Dict, Iterable, List

from openai import OpenAI


def _load_input(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _iter_records(payload: Any) -> Iterable[Dict[str, Any]]:
    if isinstance(payload, list):
        for item in payload:
            if isinstance(item, dict):
                yield item
        return
    if isinstance(payload, dict):
        for key in ("results", "items", "records", "data", "jobs"):
            value = payload.get(key)
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        yield item
                return
        yield payload


def _extract_numbers(records: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    total = 0
    completed = 0
    failed = 0
    skipped = 0
    dimensions: List[int] = []
    model_counts: Dict[str, int] = {}
    error_counts: Dict[str, int] = {}

    for record in records:
        total += 1
        status = str(record.get("status", record.get("state", ""))).lower()
        if status in {"completed", "success", "succeeded", "done"}:
            completed += 1
        elif status in {"failed", "error", "errored"}:
            failed += 1
        elif status in {"skipped", "ignored"}:
            skipped += 1

        dims = record.get("dimensions") or record.get("dimension")
        if isinstance(dims, int):
            dimensions.append(dims)

        model = record.get("model")
        if isinstance(model, str) and model:
            model_counts[model] = model_counts.get(model, 0) + 1

        err = record.get("error") or record.get("error_type")
        if isinstance(err, str) and err:
            error_counts[err] = error_counts.get(err, 0) + 1

    return {
        "total": total,
        "completed": completed,
        "failed": failed,
        "skipped": skipped,
        "dimensions": dimensions,
        "model_counts": model_counts,
        "error_counts": error_counts,
    }


def _build_summary(stats: Dict[str, Any]) -> str:
    dim_text = "unknown"
    if stats["dimensions"]:
        avg = sum(stats["dimensions"]) / len(stats["dimensions"])
        dim_text = f"avg {avg:.1f}, min {min(stats['dimensions'])}, max {max(stats['dimensions'])}"

    top_model = "unknown"
    if stats["model_counts"]:
        top_model = max(stats["model_counts"], key=stats["model_counts"].get)

    top_error = "none"
    if stats["error_counts"]:
        top_error = max(stats["error_counts"], key=stats["error_counts"].get)

    return (
        f"Embedding job summary: {stats['completed']}/{stats['total']} completed, "
        f"{stats['failed']} failed, {stats['skipped']} skipped. "
        f"Dimensions: {dim_text}. Top model: {top_model}. Top error: {top_error}."
    )


def summarize_embedding_job(input_path: str) -> str:
    payload = _load_input(input_path)
    stats = _extract_numbers(_iter_records(payload))
    summary = _build_summary(stats)

    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        client = OpenAI(api_key=api_key)
        response = client.responses.create(
            model="gpt-5.4-mini",
            input=(
                "Summarize this embedding job result in one concise sentence, "
                "mentioning completion status, failures, and any notable quality signals:\n"
                f"{summary}"
            ),
        )
        text = getattr(response, "output_text", None)
        if isinstance(text, str) and text.strip():
            return text.strip()
    return summary


def main() -> None:
    import sys

    if len(sys.argv) < 2:
        raise SystemExit("usage: embedding_job_summary.py <input.json>")
    print(summarize_embedding_job(sys.argv[1]))


if __name__ == "__main__":
    main()
