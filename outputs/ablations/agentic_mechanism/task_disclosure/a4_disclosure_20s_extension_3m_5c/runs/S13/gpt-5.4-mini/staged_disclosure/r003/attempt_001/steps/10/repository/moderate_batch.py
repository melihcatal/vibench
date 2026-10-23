import os
from typing import Any, Dict, List

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def moderate_batch(messages: List[str]) -> List[Dict[str, Any]]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODERATION_MODEL,
            "input": messages,
        },
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    results = payload["results"]
    decisions: List[Dict[str, Any]] = []
    for index, result in enumerate(results):
        categories = result.get("categories", {})
        category_scores = result.get("category_scores", {})
        flagged = bool(result.get("flagged", False))
        unsafe_categories = [name for name, value in categories.items() if value]
        decisions.append(
            {
                "index": index,
                "flagged": flagged,
                "unsafe_categories": unsafe_categories,
                "category_scores": category_scores,
                "raw": result,
            }
        )
    return decisions


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        raise SystemExit("usage: moderate_batch.py TEXT [TEXT ...]")
    print(moderate_batch(sys.argv[1:]))
