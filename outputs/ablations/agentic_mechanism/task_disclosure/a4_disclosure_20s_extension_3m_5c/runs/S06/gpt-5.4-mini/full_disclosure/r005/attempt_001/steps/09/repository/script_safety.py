import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_INPUT_SAFETY_MODEL = "omni-moderation-latest"


def check_script_safety(script: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json={"model": OPENAI_INPUT_SAFETY_MODEL, "input": script},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()

    results: List[Dict[str, Any]] = payload.get("results", [])
    result = results[0] if results else {}
    categories = result.get("categories", {})
    category_scores = result.get("category_scores", {})

    unsafe_categories = [name for name, flagged in categories.items() if flagged]

    return {
        "provider": "openai",
        "model": OPENAI_INPUT_SAFETY_MODEL,
        "flagged": bool(result.get("flagged", False)),
        "unsafe_categories": unsafe_categories,
        "category_scores": category_scores,
        "raw": payload,
    }
