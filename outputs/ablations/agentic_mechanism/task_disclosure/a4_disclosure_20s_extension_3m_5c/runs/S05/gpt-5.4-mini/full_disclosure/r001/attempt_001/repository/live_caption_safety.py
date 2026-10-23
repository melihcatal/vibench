import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"


def check_live_caption_safety(text: str, model: str = "omni-moderation-latest") -> Dict[str, Any]:
    api_key = os.getenv(OPENAI_API_KEY_ENV)
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": model, "input": text},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    result = data["results"][0]
    categories = result.get("categories", {})
    category_scores = result.get("category_scores", {})
    flagged = bool(result.get("flagged", False))
    unsafe_categories = [name for name, enabled in categories.items() if enabled]
    return {
        "flagged": flagged,
        "unsafe_categories": unsafe_categories,
        "category_scores": category_scores,
        "raw": result,
    }


def is_caption_safe(text: str, model: str = "omni-moderation-latest") -> bool:
    return not check_live_caption_safety(text, model=model)["flagged"]
