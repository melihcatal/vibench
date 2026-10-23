import os
from typing import Iterable, List, Optional

from openai import OpenAI


def _get_client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def _safe_float(value: object) -> Optional[float]:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def summarize_embedding_job_results(job_results: Iterable[dict]) -> str:
    results: List[dict] = list(job_results)
    total = len(results)
    succeeded = 0
    failed = 0
    total_tokens = 0
    dimensions = []
    model_counts = {}
    error_messages = []

    for item in results:
        status = str(item.get("status", "")).lower()
        if status in {"succeeded", "success", "completed", "done"}:
            succeeded += 1
        else:
            failed += 1

        tokens = _safe_float(item.get("usage_tokens") or item.get("tokens") or item.get("token_count"))
        if tokens is not None:
            total_tokens += int(tokens)

        dim = _safe_float(item.get("dimensions") or item.get("dimension"))
        if dim is not None:
            dimensions.append(int(dim))

        model = item.get("model")
        if model:
            model_counts[str(model)] = model_counts.get(str(model), 0) + 1

        error = item.get("error") or item.get("message")
        if error:
            error_messages.append(str(error))

    average_dimension = int(sum(dimensions) / len(dimensions)) if dimensions else None
    dominant_model = max(model_counts, key=model_counts.get) if model_counts else None

    summary_lines = [
        f"Embedding job summary (OpenAI):",
        f"- total jobs: {total}",
        f"- succeeded: {succeeded}",
        f"- failed: {failed}",
        f"- total tokens: {total_tokens}",
    ]

    if average_dimension is not None:
        summary_lines.append(f"- average dimensions: {average_dimension}")
    if dominant_model is not None:
        summary_lines.append(f"- most common model: {dominant_model}")
    if error_messages:
        summary_lines.append(f"- errors: {'; '.join(error_messages[:5])}")

    return "\n".join(summary_lines)


def summarize_with_openai(job_results: Iterable[dict]) -> str:
    client = _get_client()
    summary = summarize_embedding_job_results(job_results)
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {
                "role": "system",
                "content": "You summarize embedding job results concisely.",
            },
            {
                "role": "user",
                "content": summary,
            },
        ],
    )
    return response.output_text
