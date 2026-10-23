import os
from typing import Any, Dict, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/moderations"
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def check_unsafe_content(text: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    if not text:
        return {"unsafe": False, "categories": {}, "category_scores": {}, "flagged": False}

    key = api_key or os.getenv(OPENAI_API_KEY_ENV)
    if not key:
        raise ValueError("Missing OpenAI API key")

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json={"model": OPENAI_MODERATION_MODEL, "input": text},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    result = data["results"][0]
    return {
        "unsafe": bool(result.get("flagged", False)),
        "flagged": bool(result.get("flagged", False)),
        "categories": result.get("categories", {}),
        "category_scores": result.get("category_scores", {}),
        "raw": data,
    }
