import json
import os
from typing import Any, Dict

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def moderate_text(text: str) -> Dict[str, Any]:
    api_key = os.getenv(OPENAI_API_KEY_ENV)
    if not api_key:
        raise RuntimeError("Missing OPENAI_API_KEY")
    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        data=json.dumps({"model": OPENAI_MODERATION_MODEL, "input": text}),
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    result = payload["results"][0]
    categories = result.get("categories", {})
    category_scores = result.get("category_scores", {})
    flagged = bool(result.get("flagged", False))
    score = max(category_scores.values(), default=0.0)
    return {
        "flagged": flagged,
        "score": score,
        "categories": categories,
        "category_scores": category_scores,
        "raw": payload,
    }


if __name__ == "__main__":
    import sys

    text = sys.stdin.read()
    print(json.dumps(moderate_text(text), ensure_ascii=False))
