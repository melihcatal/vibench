import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def moderate_vendor_notes(text: str, categories: Optional[List[str]] = None) -> Dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload: Dict[str, Any] = {"model": OPENAI_MODERATION_MODEL, "input": text}
    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    result = data["results"][0]
    categories_found = result.get("categories", {})
    category_scores = result.get("category_scores", {})

    if categories:
        filtered_categories = {k: categories_found.get(k) for k in categories if k in categories_found}
        filtered_scores = {k: category_scores.get(k) for k in categories if k in category_scores}
    else:
        filtered_categories = categories_found
        filtered_scores = category_scores

    return {
        "flagged": result.get("flagged", False),
        "categories": filtered_categories,
        "category_scores": filtered_scores,
        "raw": result,
    }


def is_safe_vendor_text(text: str) -> bool:
    return not moderate_vendor_notes(text).get("flagged", False)
