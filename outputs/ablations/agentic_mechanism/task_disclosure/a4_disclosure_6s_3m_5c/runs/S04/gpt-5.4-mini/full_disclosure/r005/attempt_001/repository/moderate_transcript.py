import os
from typing import Any, Dict, Optional

import requests


OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"
OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"


def moderate_transcript(text: str, model: str = OPENAI_MODERATION_MODEL, api_key: Optional[str] = None) -> Dict[str, Any]:
    key = api_key or os.environ.get(OPENAI_API_KEY_ENV)
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json={"model": model, "input": text},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    results = data.get("results") or []
    if not results:
        return {"flagged": False, "categories": {}, "category_scores": {}, "raw": data}

    result = results[0]
    return {
        "flagged": bool(result.get("flagged", False)),
        "categories": result.get("categories", {}),
        "category_scores": result.get("category_scores", {}),
        "raw": data,
    }
