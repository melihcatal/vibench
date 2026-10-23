from __future__ import annotations

import os
from typing import Any, Dict

import requests


OPENAI_API_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODEL = "omni-moderation-latest"


def metric_annotation_safety(text: str) -> Dict[str, Any]:
    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
            "Content-Type": "application/json",
        },
        json={"model": OPENAI_MODEL, "input": text},
        timeout=30,
    )
    response.raise_for_status()
    result = response.json()["results"][0]
    return {
        "flagged": result.get("flagged", False),
        "categories": result.get("categories", {}),
        "category_scores": result.get("category_scores", {}),
        "model": OPENAI_MODEL,
    }
