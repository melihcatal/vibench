from __future__ import annotations

import os
from typing import Any, Dict

import requests


OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_MODERATIONS_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def moderate_claim_text(text: str) -> Dict[str, Any]:
    response = requests.post(
        OPENAI_MODERATIONS_URL,
        headers={
            "Authorization": f"Bearer {os.environ[OPENAI_API_KEY_ENV]}",
            "Content-Type": "application/json",
        },
        json={"model": OPENAI_MODERATION_MODEL, "input": text},
        timeout=30,
    )
    response.raise_for_status()
    result = response.json()["results"][0]
    return {
        "provider": "openai",
        "model": OPENAI_MODERATION_MODEL,
        "flagged": result.get("flagged", False),
        "categories": result.get("categories", {}),
        "category_scores": result.get("category_scores", {}),
    }
