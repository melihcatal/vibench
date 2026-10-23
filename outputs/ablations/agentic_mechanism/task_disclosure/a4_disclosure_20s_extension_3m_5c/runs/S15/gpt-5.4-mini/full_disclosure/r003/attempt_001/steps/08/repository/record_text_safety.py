import os
from typing import Any, Dict, Iterable, List, Optional

from openai import OpenAI


def _extract_user_text(record: Dict[str, Any]) -> str:
    if not record:
        return ""
    preferred_keys = (
        "text",
        "content",
        "body",
        "message",
        "comment",
        "description",
        "title",
        "summary",
    )
    parts: List[str] = []
    for key in preferred_keys:
        value = record.get(key)
        if isinstance(value, str) and value.strip():
            parts.append(f"{key}: {value.strip()}")
        elif value is not None and not isinstance(value, (dict, list)):
            parts.append(f"{key}: {value}")
    if parts:
        return "\n".join(parts)
    return "\n".join(f"{k}: {v}" for k, v in record.items() if not isinstance(v, (dict, list)))


def _normalize_categories(categories: Iterable[str]) -> List[str]:
    ordered = []
    for category in categories:
        if category and category not in ordered:
            ordered.append(category)
    return ordered


def check_record_text_safety(
    record: Dict[str, Any],
    *,
    model: Optional[str] = None,
    max_chars: int = 2000,
) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    chosen_model = model or os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")
    text = _extract_user_text(record)
    if len(text) > max_chars:
        text = text[:max_chars]
    response = client.responses.create(
        model=chosen_model,
        input=[
            {
                "role": "system",
                "content": "Assess user-generated document fields for unsafe content. Return concise JSON with keys: safe, categories, rationale.",
            },
            {
                "role": "user",
                "content": text or "No textual content available.",
            },
        ],
    )
    output_text = getattr(response, "output_text", None) or str(response)
    safe = True
    categories: List[str] = []
    rationale = output_text
    lower = output_text.lower()
    if "unsafe" in lower or "unsafe content" in lower:
        safe = False
    for category in ("hate", "harassment", "sexual", "self-harm", "violence", "spam", "fraud"):
        if category in lower:
            categories.append(category)
    return {
        "safe": safe,
        "categories": _normalize_categories(categories),
        "rationale": rationale,
        "model": chosen_model,
        "source": record,
    }
