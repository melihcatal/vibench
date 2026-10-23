import os
from typing import Any, Dict

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def check_message_safety(payload_text: str) -> Dict[str, Any]:
    if not isinstance(payload_text, str):
        raise TypeError("payload_text must be a string")
    if not payload_text.strip():
        return {"safe": True, "flagged": False, "categories": {}, "category_scores": {}, "provider": "openai", "model": OPENAI_MODERATION_MODEL}

    headers = {"Content-Type": "application/json"}
    if OPENAI_API_KEY:
        headers["Authorization"] = f"Bearer {OPENAI_API_KEY}"

    response = requests.post(
        OPENAI_MODERATION_URL,
        headers=headers,
        json={"model": OPENAI_MODERATION_MODEL, "input": payload_text},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    result = (data.get("results") or [{}])[0]
    flagged = bool(result.get("flagged", False))
    return {
        "safe": not flagged,
        "flagged": flagged,
        "categories": result.get("categories", {}),
        "category_scores": result.get("category_scores", {}),
        "provider": "openai",
        "model": OPENAI_MODERATION_MODEL,
    }
