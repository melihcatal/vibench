from __future__ import annotations

import os
from typing import Any, Dict

import requests


def check_ocr_safety(text: str) -> Dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Missing required environment variable: OPENAI_API_KEY")
    response = requests.post(
        "https://api.openai.com/v1/moderations",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={"model": "omni-moderation-latest", "input": text},
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    result = payload["results"][0]
    return {
        "provider": "openai",
        "model": "omni-moderation-latest",
        "flagged": result.get("flagged", False),
        "categories": result.get("categories", {}),
        "category_scores": result.get("category_scores", {}),
    }
