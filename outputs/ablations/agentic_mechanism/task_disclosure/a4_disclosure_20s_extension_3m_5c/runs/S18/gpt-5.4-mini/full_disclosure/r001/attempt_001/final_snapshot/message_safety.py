import os
from typing import Any, Dict, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


def check_message_payload_text(payload_text: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    token = api_key or os.getenv("OPENAI_API_KEY")
    if not token:
        raise ValueError("OPENAI_API_KEY is required")

    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={"model": OPENAI_MODEL, "input": payload_text},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()

    result = data["results"][0]
    categories = result.get("categories", {})
    category_scores = result.get("category_scores", {})
    flagged = bool(result.get("flagged", False))

    unsafe_categories = [name for name, is_unsafe in categories.items() if is_unsafe]

    return {
        "provider": "openai",
        "model": OPENAI_MODEL,
        "flagged": flagged,
        "unsafe_categories": unsafe_categories,
        "categories": categories,
        "category_scores": category_scores,
        "raw": data,
    }
