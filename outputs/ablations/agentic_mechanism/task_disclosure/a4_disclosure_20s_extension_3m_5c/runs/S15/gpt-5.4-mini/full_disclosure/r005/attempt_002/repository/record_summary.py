import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = os.getenv("OPENAI_API_URL", "https://api.openai.com/v1/chat/completions")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "openai/gpt-5.4-mini")


def _coerce_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (int, float, bool)):
        return str(value)
    if isinstance(value, dict):
        parts: List[str] = []
        for key in sorted(value.keys()):
            parts.append(f"{key}: {_coerce_text(value[key])}")
        return " | ".join(parts)
    if isinstance(value, list):
        return ", ".join(_coerce_text(item) for item in value)
    return str(value)


def _normalize_record(record: Dict[str, Any]) -> Dict[str, Any]:
    normalized = dict(record)
    for key in ("id", "identifier", "title", "name", "summary", "description", "content", "text"):
        if key in normalized and normalized[key] is not None:
            normalized[key] = _coerce_text(normalized[key]).strip()
    return normalized


def summarize_record(record: Dict[str, Any], max_summary_chars: int = 400, temperature: float = 0.2) -> Dict[str, Any]:
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is required")

    normalized = _normalize_record(record)
    prompt = (
        "Summarize the following document record for a user. "
        "Return concise, neutral prose and include the most important facts.\n\n"
        f"Record:\n{normalized}"
    )

    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": "You summarize document records succinctly and accurately."},
            {"role": "user", "content": prompt},
        ],
        "temperature": temperature,
    }

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    summary = data["choices"][0]["message"]["content"].strip()

    if max_summary_chars > 0 and len(summary) > max_summary_chars:
        summary = summary[: max(0, max_summary_chars - 1)].rstrip() + "…"

    return {
        "provider": "openai",
        "model": OPENAI_MODEL,
        "summary": summary,
        "usage": data.get("usage", {}),
    }


def summarize_records(records: List[Dict[str, Any]], max_summary_chars: int = 400) -> List[Dict[str, Any]]:
    return [summarize_record(record, max_summary_chars=max_summary_chars) for record in records]
