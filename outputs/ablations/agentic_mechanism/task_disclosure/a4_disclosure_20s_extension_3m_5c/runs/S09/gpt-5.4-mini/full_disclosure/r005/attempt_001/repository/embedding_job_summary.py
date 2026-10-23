import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


def _safe_get(obj: Any, key: str, default: Any = None) -> Any:
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def _extract_text(payload: Any) -> str:
    if payload is None:
        return ""
    if isinstance(payload, str):
        return payload.strip()
    if isinstance(payload, list):
        parts = []
        for item in payload:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                text = item.get("text") or item.get("content") or item.get("value")
                if text:
                    parts.append(str(text))
            else:
                text = getattr(item, "text", None) or getattr(item, "content", None) or getattr(item, "value", None)
                if text:
                    parts.append(str(text))
        return "\n".join(p.strip() for p in parts if p and str(p).strip())
    if isinstance(payload, dict):
        for key in ("text", "content", "summary", "result", "message"):
            value = payload.get(key)
            if value:
                extracted = _extract_text(value)
                if extracted:
                    return extracted
        return str(payload)
    for key in ("text", "content", "summary", "result", "message"):
        value = getattr(payload, key, None)
        if value:
            extracted = _extract_text(value)
            if extracted:
                return extracted
    return str(payload)


def _collect_stats(job_result: Any) -> Dict[str, Any]:
    stats = {}
    for key in (
        "total",
        "processed",
        "succeeded",
        "failed",
        "skipped",
        "queued",
        "completed",
        "input_tokens",
        "output_tokens",
        "cost",
        "model",
    ):
        value = _safe_get(job_result, key)
        if value is not None:
            stats[key] = value
    return stats


def summarize_embedding_job(job_result: Any) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    model = os.environ.get("OPENAI_SUMMARY_MODEL", "gpt-5.4-mini")

    stats = _collect_stats(job_result)
    raw_text = _extract_text(_safe_get(job_result, "results", _safe_get(job_result, "items", job_result)))
    payload = {
        "stats": stats,
        "results": raw_text[:20000],
    }

    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": "Summarize embedding job results concisely with totals, failures, notable patterns, and recommended follow-ups.",
            },
            {
                "role": "user",
                "content": f"Summarize this embedding job result data as a compact operational report:\n{payload}",
            },
        ],
    )
    return _extract_text(response.output_text)


def main(job_result: Optional[Any] = None) -> str:
    if job_result is None:
        return summarize_embedding_job({})
    return summarize_embedding_job(job_result)
