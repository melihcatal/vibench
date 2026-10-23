import json
import os
from typing import Any, Dict, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
DEFAULT_OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def _moderate(text: str, model: Optional[str] = None) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload = {"input": text}
    if model:
        payload["model"] = model
    else:
        payload["model"] = DEFAULT_OPENAI_MODERATION_MODEL

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
    return response.json()


def check_prompt(prompt: str) -> Dict[str, Any]:
    result = _moderate(prompt)
    item = result["results"][0]
    return {
        "safe": not item.get("flagged", False),
        "flagged": item.get("flagged", False),
        "categories": item.get("categories", {}),
        "category_scores": item.get("category_scores", {}),
        "raw": result,
    }


def check_generated_text(text: str) -> Dict[str, Any]:
    result = _moderate(text)
    item = result["results"][0]
    return {
        "safe": not item.get("flagged", False),
        "flagged": item.get("flagged", False),
        "categories": item.get("categories", {}),
        "category_scores": item.get("category_scores", {}),
        "raw": result,
    }
