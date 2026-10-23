import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_SAFETY_MODEL = "omni-moderation-latest"
OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"


def check_live_caption_safety(text: str, categories: Optional[List[str]] = None) -> Dict[str, Any]:
    api_key = os.environ.get(OPENAI_API_KEY_ENV)
    if not api_key:
        raise RuntimeError(f"Missing required environment variable: {OPENAI_API_KEY_ENV}")

    payload: Dict[str, Any] = {"model": OPENAI_SAFETY_MODEL, "input": text}
    if categories:
        payload["categories"] = categories

    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()

    results = data.get("results") or []
    result = results[0] if results else {}
    flagged = bool(result.get("flagged", False))
    categories_out = result.get("categories", {})
    category_scores = result.get("category_scores", {})

    return {
        "flagged": flagged,
        "categories": categories_out,
        "category_scores": category_scores,
        "raw": data,
    }
