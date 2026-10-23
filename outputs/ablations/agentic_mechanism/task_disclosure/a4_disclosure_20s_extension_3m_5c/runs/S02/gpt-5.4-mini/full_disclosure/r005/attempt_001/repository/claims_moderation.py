import json
import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"


def moderate_claims(text: str, api_key: Optional[str] = None, model: str = "omni-moderation-latest") -> Dict[str, Any]:
    key = api_key or os.environ.get("OPENAI_API_KEY")
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
    payload = response.json()
    result = (payload.get("results") or [{}])[0]
    categories = result.get("categories") or {}
    category_scores = result.get("category_scores") or {}

    flagged_categories: List[str] = [name for name, flagged in categories.items() if flagged]

    return {
        "provider": "openai",
        "model": model,
        "flagged": bool(result.get("flagged")),
        "flagged_categories": flagged_categories,
        "category_scores": category_scores,
        "raw": payload,
    }


def moderate_claims_json(text: str, api_key: Optional[str] = None, model: str = "omni-moderation-latest") -> str:
    return json.dumps(moderate_claims(text, api_key=api_key, model=model))
