import os
from typing import Any, Dict, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"


def check_log_text_safety(text: str, model: str = "omni-moderation-latest") -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={"model": model, "input": text},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()

    result = payload["results"][0]
    categories = result.get("categories", {})
    category_scores = result.get("category_scores", {})
    flagged = bool(result.get("flagged", False))

    return {
        "flagged": flagged,
        "categories": categories,
        "category_scores": category_scores,
        "raw": payload,
    }


def is_log_text_safe(text: str, model: str = "omni-moderation-latest") -> bool:
    return not check_log_text_safety(text, model=model)["flagged"]
