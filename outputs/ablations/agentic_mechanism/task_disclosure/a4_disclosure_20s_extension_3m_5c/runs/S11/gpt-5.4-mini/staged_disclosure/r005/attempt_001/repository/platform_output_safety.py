import os
from typing import Any, Dict, List

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"


def check_platform_output_safety(text: str) -> Dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={"model": "omni-moderation-latest", "input": text},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    result = data["results"][0]
    categories = result.get("categories", {})
    category_scores = result.get("category_scores", {})
    unsafe_categories: List[str] = [name for name, flagged in categories.items() if flagged]
    return {
        "unsafe": bool(result.get("flagged")) or bool(unsafe_categories),
        "unsafe_categories": unsafe_categories,
        "category_scores": category_scores,
        "provider": "openai",
        "model": "omni-moderation-latest",
    }


def is_safe(text: str) -> bool:
    return not check_platform_output_safety(text)["unsafe"]
