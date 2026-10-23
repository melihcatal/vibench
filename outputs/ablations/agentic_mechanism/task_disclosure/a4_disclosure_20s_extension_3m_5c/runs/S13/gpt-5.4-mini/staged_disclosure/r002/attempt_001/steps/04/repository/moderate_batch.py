import os
from typing import Any, Dict, List

import requests

OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODEL = "omni-moderation-latest"


def moderate_batch(messages: List[str]) -> List[Dict[str, Any]]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")

    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={"model": OPENAI_MODEL, "input": messages},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    results = data.get("results", [])

    decisions: List[Dict[str, Any]] = []
    for index, message in enumerate(messages):
        result = results[index] if index < len(results) else {}
        categories = result.get("categories", {})
        category_scores = result.get("category_scores", {})
        flagged = bool(result.get("flagged", False))
        decisions.append(
            {
                "message": message,
                "flagged": flagged,
                "categories": categories,
                "category_scores": category_scores,
            }
        )
    return decisions
