import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def _extract_text(labels: Any) -> str:
    if labels is None:
        return ""
    if isinstance(labels, str):
        return labels
    if isinstance(labels, dict):
        for key in ("text", "label", "name", "description", "caption"):
            value = labels.get(key)
            if isinstance(value, str) and value.strip():
                return value
        parts: List[str] = []
        for value in labels.values():
            if isinstance(value, str) and value.strip():
                parts.append(value)
        return " ".join(parts)
    if isinstance(labels, (list, tuple, set)):
        return " ".join(_extract_text(item) for item in labels if _extract_text(item))
    return str(labels)


def _normalize_response(data: Dict[str, Any]) -> Dict[str, Any]:
    result = data.get("results", [{}])[0] if isinstance(data, dict) else {}
    categories = result.get("categories", {}) if isinstance(result, dict) else {}
    category_scores = result.get("category_scores", {}) if isinstance(result, dict) else {}
    flagged = bool(result.get("flagged", False)) if isinstance(result, dict) else False
    unsafe_categories = [name for name, is_flagged in categories.items() if bool(is_flagged)]
    return {
        "provider": "openai",
        "model": OPENAI_MODERATION_MODEL,
        "flagged": flagged,
        "unsafe_categories": unsafe_categories,
        "category_scores": category_scores,
        "raw": data,
    }


def check_generated_visual_labels(labels: Any, api_key: Optional[str] = None, timeout: float = 30.0) -> Dict[str, Any]:
    text = _extract_text(labels).strip()
    if not text:
        return {
            "provider": "openai",
            "model": OPENAI_MODERATION_MODEL,
            "flagged": False,
            "unsafe_categories": [],
            "category_scores": {},
            "raw": {"results": []},
        }

    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json={"model": OPENAI_MODERATION_MODEL, "input": text},
        timeout=timeout,
    )
    response.raise_for_status()
    return _normalize_response(response.json())
