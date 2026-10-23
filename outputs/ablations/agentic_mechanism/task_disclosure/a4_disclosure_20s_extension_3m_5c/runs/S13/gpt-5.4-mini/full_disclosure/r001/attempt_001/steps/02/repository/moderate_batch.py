import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODEL = "omni-moderation-latest"


def moderate_batch(messages: List[str], model: Optional[str] = None, api_key: Optional[str] = None) -> Dict[str, Any]:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload = {"model": model or OPENAI_MODEL, "input": messages}
    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    results = data.get("results", [])

    per_message: List[Dict[str, Any]] = []
    for index, result in enumerate(results):
        categories = result.get("categories", {})
        category_scores = result.get("category_scores", {})
        per_message.append(
            {
                "index": index,
                "flagged": bool(result.get("flagged", False)),
                "categories": categories,
                "category_scores": category_scores,
                "unsafe_categories": [name for name, value in categories.items() if value],
            }
        )

    return {
        "model": data.get("model", payload["model"]),
        "results": per_message,
        "raw": data,
    }
