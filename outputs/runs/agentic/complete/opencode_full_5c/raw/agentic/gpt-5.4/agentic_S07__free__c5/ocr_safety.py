from __future__ import annotations

import os
from typing import Any, Dict

import requests


OPENAI_MODERATIONS_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def check_ocr_text_safety(text: str) -> Dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    response = requests.post(
        OPENAI_MODERATIONS_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={"model": OPENAI_MODERATION_MODEL, "input": text},
        timeout=60,
    )
    response.raise_for_status()
    result = response.json()["results"][0]
    return {
        "flagged": result["flagged"],
        "categories": result["categories"],
        "category_scores": result["category_scores"],
    }
