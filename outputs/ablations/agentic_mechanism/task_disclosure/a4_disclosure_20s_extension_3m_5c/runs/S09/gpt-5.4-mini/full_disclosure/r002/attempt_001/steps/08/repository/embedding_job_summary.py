import os
from typing import Any, Dict, Iterable, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
DEFAULT_MODEL = "gpt-5.4-mini"


def _format_number(value: Any) -> str:
    if isinstance(value, bool) or value is None:
        return str(value)
    if isinstance(value, int):
        return f"{value:,}"
    if isinstance(value, float):
        return f"{value:,.4f}".rstrip("0").rstrip(".")
    return str(value)


def _safe_get(mapping: Dict[str, Any], keys: Iterable[str], default: Any = None) -> Any:
    for key in keys:
        if key in mapping and mapping[key] is not None:
            return mapping[key]
    return default


def _extract_text(response_json: Dict[str, Any]) -> str:
    if isinstance(response_json.get("output_text"), str) and response_json["output_text"].strip():
        return response_json["output_text"].strip()
    output = response_json.get("output", [])
    parts: List[str] = []
    for item in output:
        if not isinstance(item, dict):
            continue
        for content in item.get("content", []):
            if isinstance(content, dict) and content.get("type") in {"output_text", "text"}:
                text = content.get("text")
                if isinstance(text, str):
                    parts.append(text)
    return "\n".join(part.strip() for part in parts if part.strip())


def summarize_embedding_job(job_result: Dict[str, Any], model: Optional[str] = None) -> str:
    total = _safe_get(job_result, ["total_texts", "total", "count"], 0)
    succeeded = _safe_get(job_result, ["succeeded", "success", "embedded"], 0)
    failed = _safe_get(job_result, ["failed", "errors", "error_count"], 0)
    skipped = _safe_get(job_result, ["skipped", "filtered", "dropped"], 0)
    duration = _safe_get(job_result, ["duration_seconds", "elapsed_seconds", "runtime_seconds"], None)
    dimensions = _safe_get(job_result, ["dimensions", "embedding_dimensions", "vector_size"], None)
    provider = _safe_get(job_result, ["provider", "service"], "OpenAI")
    job_name = _safe_get(job_result, ["job_name", "name", "id"], "embedding job")

    prompt = (
        f"Summarize this embedding job result for a concise status report.\n"
        f"Provider: {provider}\n"
        f"Job: {job_name}\n"
        f"Total texts: {_format_number(total)}\n"
        f"Succeeded: {_format_number(succeeded)}\n"
        f"Failed: {_format_number(failed)}\n"
        f"Skipped: {_format_number(skipped)}\n"
        f"Duration seconds: {_format_number(duration)}\n"
        f"Embedding dimensions: {_format_number(dimensions)}\n"
        f"Return 2-4 short bullet points and mention any notable issues or throughput observations if inferable."
    )

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return (
            f"{provider} embedding job {job_name}: "
            f"{_format_number(succeeded)}/{_format_number(total)} succeeded, "
            f"{_format_number(failed)} failed, {_format_number(skipped)} skipped"
            + (f", {_format_number(duration)}s" if duration is not None else "")
            + (f", { _format_number(dimensions) } dims" if dimensions is not None else "")
        )

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model or DEFAULT_MODEL,
            "input": prompt,
        },
        timeout=60,
    )
    response.raise_for_status()
    return _extract_text(response.json())
