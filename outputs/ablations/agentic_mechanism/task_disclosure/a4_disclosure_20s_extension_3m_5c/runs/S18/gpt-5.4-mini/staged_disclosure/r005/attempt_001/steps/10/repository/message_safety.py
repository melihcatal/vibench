import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODEL = "omni-moderation-latest"


def _extract_text(payload: Any) -> str:
    if isinstance(payload, str):
        return payload
    if isinstance(payload, dict):
        for key in ("text", "content", "message", "body", "payload"):
            value = payload.get(key)
            if isinstance(value, str):
                return value
            if isinstance(value, list):
                pieces = []
                for item in value:
                    if isinstance(item, str):
                        pieces.append(item)
                    elif isinstance(item, dict):
                        for nested_key in ("text", "content", "body"):
                            nested_value = item.get(nested_key)
                            if isinstance(nested_value, str):
                                pieces.append(nested_value)
                                break
                if pieces:
                    return " ".join(pieces)
    return str(payload)


def check_message_safety(payload: Any, api_key: Optional[str] = None) -> Dict[str, Any]:
    text = _extract_text(payload)
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")

    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={"model": OPENAI_MODEL, "input": text},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    result = (data.get("results") or [{}])[0]
    categories = result.get("categories") or {}
    category_scores = result.get("category_scores") or {}
    unsafe = bool(result.get("flagged"))
    return {
        "unsafe": unsafe,
        "categories": categories,
        "category_scores": category_scores,
        "provider": "openai",
        "model": OPENAI_MODEL,
        "text": text,
    }
