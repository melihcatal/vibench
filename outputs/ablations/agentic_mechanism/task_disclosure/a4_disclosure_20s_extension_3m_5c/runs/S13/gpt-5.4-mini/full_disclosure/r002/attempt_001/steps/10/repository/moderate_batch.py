import os
from typing import Any, Dict, List, Optional, Sequence

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def moderate_batch(messages: Sequence[str], model: str = OPENAI_MODERATION_MODEL, api_key: Optional[str] = None) -> List[Dict[str, Any]]:
    token = api_key or os.getenv("OPENAI_API_KEY")
    if not token:
        raise ValueError("OPENAI_API_KEY is required")

    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json={"model": model, "input": list(messages)},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    results = payload.get("results", [])

    decisions: List[Dict[str, Any]] = []
    for index, message in enumerate(messages):
        result = results[index] if index < len(results) else {}
        decisions.append(
            {
                "message": message,
                "model": model,
                "flagged": result.get("flagged", False),
                "categories": result.get("categories", {}),
                "category_scores": result.get("category_scores", {}),
                "raw": result,
            }
        )
    return decisions


def moderate_batch_from_env(messages: Sequence[str]) -> List[Dict[str, Any]]:
    return moderate_batch(messages)
