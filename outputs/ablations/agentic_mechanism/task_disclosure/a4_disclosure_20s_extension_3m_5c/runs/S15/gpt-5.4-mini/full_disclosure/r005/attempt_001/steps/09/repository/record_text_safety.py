import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_DEFAULT_MODEL = "omni-moderation-latest"


def _to_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (int, float, bool)):
        return str(value)
    if isinstance(value, dict):
        parts: List[str] = []
        for key in sorted(value.keys()):
            parts.append(f"{key}: {_to_text(value[key])}")
        return "\n".join(part for part in parts if part)
    if isinstance(value, (list, tuple, set)):
        return "\n".join(_to_text(item) for item in value if _to_text(item))
    return str(value)


def _collect_user_text(record: Dict[str, Any]) -> str:
    preferred_keys = (
        "text",
        "content",
        "message",
        "body",
        "description",
        "title",
        "summary",
        "notes",
    )
    collected: List[str] = []
    for key in preferred_keys:
        if key in record:
            text = _to_text(record.get(key)).strip()
            if text:
                collected.append(text)
    if collected:
        return "\n".join(collected)
    return _to_text(record).strip()


def _moderate_text(text: str, api_key: str, model: str) -> Dict[str, Any]:
    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={"model": model, "input": text},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def record_text_safety(record: Dict[str, Any], api_key: Optional[str] = None, model: Optional[str] = None) -> Dict[str, Any]:
    key = api_key or os.getenv("OPENAI_API_KEY", "")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")
    moderation_model = model or os.getenv("OPENAI_MODERATION_MODEL", OPENAI_DEFAULT_MODEL)
    text = _collect_user_text(record)
    if not text:
        return {"safe": True, "categories": {}, "scores": {}, "flagged": False, "provider": "openai"}
    payload = _moderate_text(text, key, moderation_model)
    result = (payload.get("results") or [{}])[0]
    categories = result.get("categories") or {}
    scores = result.get("category_scores") or {}
    flagged = bool(result.get("flagged", False))
    unsafe_categories = [name for name, value in categories.items() if value]
    return {
        "safe": not flagged,
        "flagged": flagged,
        "unsafe_categories": unsafe_categories,
        "categories": categories,
        "scores": scores,
        "provider": "openai",
        "model": moderation_model,
    }
