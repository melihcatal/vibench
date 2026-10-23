import os
from typing import Any, Dict, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def _extract_text(message: Any) -> str:
    if message is None:
        return ""
    if isinstance(message, str):
        return message
    if isinstance(message, dict):
        for key in ("text", "content", "message", "payload"):
            value = message.get(key)
            if isinstance(value, str):
                return value
            if isinstance(value, dict):
                nested = _extract_text(value)
                if nested:
                    return nested
        return ""
    return str(message)


def check_message_payload_safety(message: Any, api_key: Optional[str] = None, timeout: int = 20) -> Dict[str, Any]:
    text = _extract_text(message)
    token = api_key or os.getenv("OPENAI_API_KEY")
    if not token:
        raise ValueError("OPENAI_API_KEY is required")
    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={"model": OPENAI_MODERATION_MODEL, "input": text},
        timeout=timeout,
    )
    response.raise_for_status()
    payload = response.json()
    result = (payload.get("results") or [{}])[0]
    categories = result.get("categories") or {}
    category_scores = result.get("category_scores") or {}
    flagged = bool(result.get("flagged"))
    return {
        "safe": not flagged,
        "flagged": flagged,
        "categories": categories,
        "category_scores": category_scores,
        "raw": payload,
    }
