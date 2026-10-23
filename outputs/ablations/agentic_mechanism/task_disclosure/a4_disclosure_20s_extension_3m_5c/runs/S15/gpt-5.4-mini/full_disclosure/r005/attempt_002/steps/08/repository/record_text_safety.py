import os
from typing import Any, Dict, Iterable, List, Optional

import requests


OPENAI_API_URL = os.getenv("OPENAI_API_URL", "https://api.openai.com/v1/chat/completions")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "openai/gpt-5.4-mini")


class RecordTextSafetyError(Exception):
    pass


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


def _normalize_record(record: Dict[str, Any], fields: Optional[Iterable[str]] = None) -> Dict[str, Any]:
    normalized = dict(record)
    target_fields = list(fields) if fields is not None else [
        key for key in normalized.keys() if key not in {"id", "identifier", "created_at", "updated_at", "version"}
    ]
    for key in target_fields:
        if key in normalized and normalized[key] is not None:
            normalized[key] = _coerce_text(normalized[key]).strip()
    return normalized


def check_record_text_safety(record: Dict[str, Any], fields: Optional[Iterable[str]] = None, temperature: float = 0.0) -> Dict[str, Any]:
    if not OPENAI_API_KEY:
        raise RecordTextSafetyError("OPENAI_API_KEY is required")

    normalized = _normalize_record(record, fields=fields)
    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You evaluate user-generated document text for unsafe content and return structured safety findings.",
            },
            {
                "role": "user",
                "content": (
                    "Assess the following record fields for unsafe content such as harassment, hate, self-harm, sexual content, "
                    "violent threats, or illegal instructions. Return a concise JSON object with keys: safe (boolean), "
                    "categories (array of strings), and rationale (string).\n\n"
                    f"Record:\n{normalized}"
                ),
            },
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
    content = data["choices"][0]["message"]["content"].strip()
    return {
        "provider": "openai",
        "model": OPENAI_MODEL,
        "result": content,
        "usage": data.get("usage", {}),
    }
