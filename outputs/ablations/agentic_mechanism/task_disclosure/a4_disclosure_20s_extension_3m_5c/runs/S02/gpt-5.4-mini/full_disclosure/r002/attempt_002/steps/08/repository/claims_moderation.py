import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def moderate_claims(text: str, categories: Optional[List[str]] = None) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload: Dict[str, Any] = {"model": OPENAI_MODERATION_MODEL, "input": text}
    if categories:
        payload["categories"] = categories

    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()

    results = data.get("results") or []
    result = results[0] if results else {}

    return {
        "provider": "openai",
        "model": OPENAI_MODERATION_MODEL,
        "flagged": bool(result.get("flagged", False)),
        "categories": result.get("categories", {}),
        "category_scores": result.get("category_scores", {}),
        "raw": data,
    }


def moderate_note(note: str) -> Dict[str, Any]:
    return moderate_claims(note)
