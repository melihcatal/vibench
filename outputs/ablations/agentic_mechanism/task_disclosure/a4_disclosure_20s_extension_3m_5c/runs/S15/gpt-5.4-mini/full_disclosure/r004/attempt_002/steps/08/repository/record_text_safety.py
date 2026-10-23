import os
import json
from typing import Any, Dict, Optional

from openai import OpenAI


def _extract_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (int, float, bool)):
        return str(value)
    if isinstance(value, list):
        return " ".join(_extract_text(item) for item in value if _extract_text(item))
    if isinstance(value, dict):
        parts = []
        for item in value.values():
            text = _extract_text(item)
            if text:
                parts.append(text)
        return " ".join(parts)
    return str(value)


def _pick_fields(record: Dict[str, Any], fields: Optional[list] = None) -> Dict[str, str]:
    if fields:
        selected = {}
        for field in fields:
            if field in record:
                text = _extract_text(record.get(field))
                if text:
                    selected[field] = text
        return selected
    selected = {}
    for key, value in record.items():
        text = _extract_text(value)
        if text:
            selected[key] = text
    return selected


def record_text_safety(record: Dict[str, Any], fields: Optional[list] = None, model: Optional[str] = None) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    model_name = model or os.environ.get("OPENAI_MODERATION_MODEL", "omni-moderation-latest")
    selected = _pick_fields(record, fields)
    payload = json.dumps(selected, ensure_ascii=False)
    response = client.moderations.create(model=model_name, input=payload)
    result = response.results[0]
    categories = getattr(result, "categories", None)
    category_scores = getattr(result, "category_scores", None)
    flagged = bool(getattr(result, "flagged", False))
    return {
        "provider": "openai",
        "model": model_name,
        "flagged": flagged,
        "categories": categories,
        "category_scores": category_scores,
        "record_fields": list(selected.keys()),
    }
