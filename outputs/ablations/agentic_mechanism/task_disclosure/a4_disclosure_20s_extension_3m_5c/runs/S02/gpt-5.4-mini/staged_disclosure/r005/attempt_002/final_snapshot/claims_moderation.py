import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODEL = "omni-moderation-latest"


def moderate_claim(text: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json={"model": OPENAI_MODEL, "input": text},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    result = data["results"][0]
    categories = result.get("categories", {})
    category_scores = result.get("category_scores", {})
    flagged = bool(result.get("flagged", False))

    return {
        "flagged": flagged,
        "categories": categories,
        "category_scores": category_scores,
        "provider": "openai",
        "model": OPENAI_MODEL,
        "raw": data,
    }


def moderate_claims(claims: List[str], api_key: Optional[str] = None) -> List[Dict[str, Any]]:
    return [moderate_claim(claim, api_key=api_key) for claim in claims]
