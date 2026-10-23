import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


def _extract_record_text(record: Dict[str, Any]) -> str:
    if not record:
        return ""
    preferred_keys = ("summary", "text", "content", "body", "description", "message", "title")
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


def summarize_record(record: Dict[str, Any], *, max_chars: int = 1200, model: Optional[str] = None) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    chosen_model = model or os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")
    text = _extract_record_text(record)
    if len(text) > max_chars:
        text = text[:max_chars]
    response = client.responses.create(
        model=chosen_model,
        input=[
            {
                "role": "system",
                "content": "Summarize retrieved document records concisely, preserving key facts and any actionable details.",
            },
            {
                "role": "user",
                "content": text or "No textual content available.",
            },
        ],
    )
    summary_text = getattr(response, "output_text", None)
    if not summary_text:
        summary_text = str(response)
    return {"summary": summary_text, "model": chosen_model, "source": record}
