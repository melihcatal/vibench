import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODEL = "omni-moderation-latest"


def check_log_text_safety(text: str, *, api_key: Optional[str] = None, timeout: float = 30.0) -> Dict[str, Any]:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    payload = {"model": OPENAI_MODEL, "input": text}
    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json=payload,
        timeout=timeout,
    )
    response.raise_for_status()
    data = response.json()
    result = (data.get("results") or [{}])[0]
    categories = result.get("categories") or {}
    category_scores = result.get("category_scores") or {}

    unsafe_categories: List[str] = [name for name, flagged in categories.items() if flagged]
    return {
        "provider": "openai",
        "model": OPENAI_MODEL,
        "flagged": bool(result.get("flagged", False)),
        "unsafe_categories": unsafe_categories,
        "categories": categories,
        "category_scores": category_scores,
        "raw": data,
    }
