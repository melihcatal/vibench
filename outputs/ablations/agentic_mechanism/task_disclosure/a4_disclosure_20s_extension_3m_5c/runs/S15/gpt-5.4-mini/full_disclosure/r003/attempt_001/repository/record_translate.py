import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


def _extract_translatable_text(record: Dict[str, Any]) -> str:
    if not record:
        return ""
    preferred_keys = (
        "title",
        "summary",
        "text",
        "content",
        "body",
        "description",
        "message",
        "notes",
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


def translate_record_fields(
    record: Dict[str, Any],
    *,
    target_language: str,
    model: Optional[str] = None,
    max_chars: int = 2000,
) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    chosen_model = model or os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")
    text = _extract_translatable_text(record)
    if len(text) > max_chars:
        text = text[:max_chars]
    response = client.responses.create(
        model=chosen_model,
        input=[
            {
                "role": "system",
                "content": f"Translate user-facing document fields into {target_language}. Preserve field names, meaning, and structured formatting. Return only the translated text.",
            },
            {
                "role": "user",
                "content": text or "No textual content available.",
            },
        ],
    )
    translated_text = getattr(response, "output_text", None) or str(response)
    return {
        "translated_text": translated_text,
        "target_language": target_language,
        "model": chosen_model,
        "source": record,
    }
