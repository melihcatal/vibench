from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_DEFAULT_MODEL = "omni-moderation-latest"


def moderate_text(text: str, model: Optional[str] = None, api_key: Optional[str] = None) -> Dict[str, Any]:
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not text.strip():
        raise ValueError("text must not be empty")

    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise EnvironmentError("OPENAI_API_KEY is required")

    payload = {"input": text}
    if model:
        payload["model"] = model
    else:
        payload["model"] = OPENAI_DEFAULT_MODEL

    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()

    results = data.get("results") or []
    if not results:
        return {
            "flagged": False,
            "categories": {},
            "category_scores": {},
            "raw": data,
        }

    result = results[0]
    return {
        "flagged": bool(result.get("flagged", False)),
        "categories": dict(result.get("categories") or {}),
        "category_scores": dict(result.get("category_scores") or {}),
        "raw": data,
    }


if __name__ == "__main__":
    import json
    import sys

    text = sys.stdin.read()
    output = moderate_text(text)
    print(json.dumps(output, ensure_ascii=False, indent=2))
