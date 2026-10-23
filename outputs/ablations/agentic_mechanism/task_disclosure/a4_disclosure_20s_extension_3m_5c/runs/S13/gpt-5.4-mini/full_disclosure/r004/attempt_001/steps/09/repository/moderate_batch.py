import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_MODERATION_API_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


def moderate_batch(messages: List[str], api_key: Optional[str] = None, model: Optional[str] = None) -> Dict[str, Any]:
    if not isinstance(messages, list) or any(not isinstance(message, str) for message in messages):
        raise TypeError("messages must be a list of strings")

    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload = {"model": model or OPENAI_MODERATION_MODEL, "input": messages}
    response = requests.post(
        OPENAI_MODERATION_API_URL,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    results = data.get("results") or []
    decisions = []
    for index, message in enumerate(messages):
        result = results[index] if index < len(results) else {}
        decisions.append(
            {
                "index": index,
                "message": message,
                "provider": "openai",
                "model": payload["model"],
                "flagged": bool(result.get("flagged", False)),
                "categories": result.get("categories", {}),
                "category_scores": result.get("category_scores", {}),
            }
        )
    return {"provider": "openai", "model": payload["model"], "decisions": decisions, "raw": data}
