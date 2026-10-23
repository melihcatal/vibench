import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


def _format_item(item: Dict[str, Any], index: int) -> str:
    text = str(item.get("text") or item.get("input") or item.get("content") or "")
    status = str(item.get("status") or item.get("state") or "unknown")
    error = item.get("error") or item.get("message") or ""
    vector_dims = item.get("dimensions") or item.get("embedding_dimensions")
    parts = [f"{index}. status={status}"]
    if vector_dims is not None:
        parts.append(f"dims={vector_dims}")
    if text:
        parts.append(f"text={text[:120]}")
    if error:
        parts.append(f"error={error}")
    return " | ".join(parts)


def _build_prompt(job_results: Any) -> str:
    if isinstance(job_results, list):
        items = job_results
    elif isinstance(job_results, dict) and isinstance(job_results.get("items"), list):
        items = job_results["items"]
    else:
        items = [job_results]

    lines: List[str] = []
    total = len(items)
    success = 0
    failed = 0
    for i, item in enumerate(items, start=1):
        if isinstance(item, dict):
            status = str(item.get("status") or item.get("state") or "unknown").lower()
            if status in {"succeeded", "success", "completed", "done"}:
                success += 1
            elif status in {"failed", "error", "cancelled", "canceled"}:
                failed += 1
            lines.append(_format_item(item, i))
        else:
            lines.append(f"{i}. {item}")

    return (
        "Summarize this embedding job result set concisely for an operator. "
        f"Total items: {total}. Successful: {success}. Failed: {failed}.\n\n"
        + "\n".join(lines)
    )


def summarize_embedding_job_results(job_results: Any, model: str = "gpt-5.4-mini") -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    prompt = _build_prompt(job_results)
    response = client.responses.create(
        model=model,
        input=prompt,
    )
    return response.output_text


__all__ = ["summarize_embedding_job_results"]
