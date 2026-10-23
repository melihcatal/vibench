import json
import os
from typing import Any, Dict, List

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def moderate_batch(messages: List[str]) -> List[Dict[str, Any]]:
    api_key = os.getenv(OPENAI_API_KEY_ENV)
    if not api_key:
        raise RuntimeError("Missing OPENAI_API_KEY")
    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        data=json.dumps({"model": OPENAI_MODERATION_MODEL, "input": messages}),
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    results = payload.get("results", [])
    decisions: List[Dict[str, Any]] = []
    for index, message in enumerate(messages):
        result = results[index] if index < len(results) else {}
        categories = result.get("categories", {})
        category_scores = result.get("category_scores", {})
        flagged = bool(result.get("flagged", False))
        score = max(category_scores.values(), default=0.0)
        decisions.append(
            {
                "message": message,
                "flagged": flagged,
                "score": score,
                "categories": categories,
                "category_scores": category_scores,
            }
        )
    return decisions


if __name__ == "__main__":
    import sys

    input_data = sys.stdin.read().strip()
    messages = json.loads(input_data) if input_data else []
    print(json.dumps(moderate_batch(messages), ensure_ascii=False))
