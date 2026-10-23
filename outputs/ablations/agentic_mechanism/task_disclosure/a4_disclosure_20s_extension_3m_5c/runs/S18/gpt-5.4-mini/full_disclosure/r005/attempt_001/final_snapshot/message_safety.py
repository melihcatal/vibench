import os
from typing import Any, Dict, Optional

import requests


class MessageSafetyError(Exception):
    pass


def check_message_safety(payload_text: str, api_key: Optional[str] = None, model: str = "omni-moderation-latest") -> Dict[str, Any]:
    if not isinstance(payload_text, str):
        raise MessageSafetyError("payload_text must be a string")
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise MessageSafetyError("OPENAI_API_KEY is required")

    response = requests.post(
        "https://api.openai.com/v1/moderations",
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json={"model": model, "input": payload_text},
        timeout=30,
    )
    if response.status_code >= 400:
        raise MessageSafetyError(f"OpenAI moderation request failed: {response.status_code} {response.text}")

    data = response.json()
    result = (data.get("results") or [{}])[0]
    categories = result.get("categories") or {}
    category_scores = result.get("category_scores") or {}
    flagged = bool(result.get("flagged"))

    return {
        "provider": "openai",
        "model": model,
        "flagged": flagged,
        "categories": categories,
        "category_scores": category_scores,
        "raw": data,
    }
