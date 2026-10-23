from __future__ import annotations

import os
from typing import Any, Dict

import requests


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODERATIONS_MODEL = os.getenv(
    "OPENAI_MODERATIONS_MODEL", "omni-moderation-latest"
)
OPENAI_MODERATIONS_URL = "https://api.openai.com/v1/moderations"


def vendor_text_safety(vendor_notes: str) -> Dict[str, Any]:
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is required")
    response = requests.post(
        OPENAI_MODERATIONS_URL,
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        json={"model": OPENAI_MODERATIONS_MODEL, "input": vendor_notes},
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    result = data.get("results", [{}])[0]
    return {
        "flagged": result.get("flagged", False),
        "categories": result.get("categories", {}),
        "category_scores": result.get("category_scores", {}),
        "model": OPENAI_MODERATIONS_MODEL,
    }
