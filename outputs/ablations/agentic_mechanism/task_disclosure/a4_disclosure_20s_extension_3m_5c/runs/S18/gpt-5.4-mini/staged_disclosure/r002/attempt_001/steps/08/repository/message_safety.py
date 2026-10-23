import os
from typing import Any, Dict, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


class MessageSafetyError(Exception):
    pass


def _extract_text(payload: Any) -> str:
    if payload is None:
        return ""
    if isinstance(payload, str):
        return payload
    if isinstance(payload, dict):
        for key in ("text", "message", "content", "body", "payload"):
            value = payload.get(key)
            if isinstance(value, str):
                return value
        return " ".join(str(v) for v in payload.values() if v is not None)
    return str(payload)


def check_message_payload(payload: Any, api_key: Optional[str] = None, timeout: float = 30.0) -> Dict[str, Any]:
    text = _extract_text(payload).strip()
    if not text:
        return {"safe": True, "flagged": False, "categories": {}, "model": OPENAI_MODERATION_MODEL}

    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise MessageSafetyError("OPENAI_API_KEY is required")

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
    data = response.json()
    result = (data.get("results") or [{}])[0]
    flagged = bool(result.get("flagged"))
    categories = result.get("categories") or {}
    scores = result.get("category_scores") or {}
    return {
        "safe": not flagged,
        "flagged": flagged,
        "categories": categories,
        "scores": scores,
        "model": OPENAI_MODERATION_MODEL,
    }
