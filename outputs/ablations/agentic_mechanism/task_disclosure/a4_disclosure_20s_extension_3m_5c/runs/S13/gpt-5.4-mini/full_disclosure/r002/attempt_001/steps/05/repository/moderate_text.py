import os
from typing import Any, Dict, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def moderate_text(text: str, model: str = OPENAI_MODERATION_MODEL, api_key: Optional[str] = None) -> Dict[str, Any]:
    token = api_key or os.getenv("OPENAI_API_KEY")
    if not token:
        raise ValueError("OPENAI_API_KEY is required")

    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json={"model": model, "input": text},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    result = payload["results"][0]
    return {
        "model": model,
        "flagged": result.get("flagged", False),
        "categories": result.get("categories", {}),
        "category_scores": result.get("category_scores", {}),
        "raw": payload,
    }


def moderate_text_from_env(text: str) -> Dict[str, Any]:
    return moderate_text(text)
