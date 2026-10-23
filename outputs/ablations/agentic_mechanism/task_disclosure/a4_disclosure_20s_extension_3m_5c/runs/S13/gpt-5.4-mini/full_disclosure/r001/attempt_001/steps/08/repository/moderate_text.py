import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODEL = "omni-moderation-latest"


def moderate_text(text: str, model: Optional[str] = None, api_key: Optional[str] = None) -> Dict[str, Any]:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload = {"model": model or OPENAI_MODEL, "input": text}
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
    result = data["results"][0]
    categories = result.get("categories", {})
    category_scores = result.get("category_scores", {})
    flagged = bool(result.get("flagged", False))

    unsafe_categories: List[str] = [name for name, value in categories.items() if value]

    return {
        "flagged": flagged,
        "categories": categories,
        "category_scores": category_scores,
        "unsafe_categories": unsafe_categories,
        "model": data.get("model", payload["model"]),
        "raw": data,
    }
