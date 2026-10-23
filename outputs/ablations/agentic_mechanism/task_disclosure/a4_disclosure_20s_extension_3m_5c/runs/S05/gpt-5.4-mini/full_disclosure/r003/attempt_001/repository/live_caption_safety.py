import json
import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def _auth_headers() -> Dict[str, str]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def check_live_caption_safety(text: str) -> Dict[str, Any]:
    payload = {"model": OPENAI_MODERATION_MODEL, "input": text}
    response = requests.post(OPENAI_MODERATION_URL, headers=_auth_headers(), json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    result = data["results"][0]
    return {
        "flagged": bool(result.get("flagged", False)),
        "categories": result.get("categories", {}),
        "category_scores": result.get("category_scores", {}),
        "raw": data,
    }


def unsafe_categories(result: Dict[str, Any]) -> List[str]:
    categories = result.get("categories", {})
    return [name for name, flagged in categories.items() if flagged]


def is_safe(text: str) -> bool:
    return not check_live_caption_safety(text)["flagged"]
