import os
from typing import Any, Dict, Optional

import requests


OPENAI_MODERATION_API_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


def moderate_text(text: str, api_key: Optional[str] = None, model: Optional[str] = None) -> Dict[str, Any]:
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload = {"model": model or OPENAI_MODERATION_MODEL, "input": text}
    response = requests.post(
        OPENAI_MODERATION_API_URL,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    result = (data.get("results") or [{}])[0]
    return {
        "provider": "openai",
        "model": payload["model"],
        "flagged": bool(result.get("flagged", False)),
        "categories": result.get("categories", {}),
        "category_scores": result.get("category_scores", {}),
        "raw": data,
    }
