import json
import os
from typing import Any, Dict, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/moderations"
OPENAI_TEXT_MODERATION_MODEL = "omni-moderation-latest"


def moderate_vendor_text(text: str, *, timeout: int = 30) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload = {"model": OPENAI_TEXT_MODERATION_MODEL, "input": text}
    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        data=json.dumps(payload),
        timeout=timeout,
    )
    response.raise_for_status()
    data = response.json()

    result = data["results"][0]
    categories = result.get("categories", {})
    category_scores = result.get("category_scores", {})

    return {
        "provider": "openai",
        "model": OPENAI_TEXT_MODERATION_MODEL,
        "flagged": bool(result.get("flagged", False)),
        "categories": categories,
        "category_scores": category_scores,
        "raw": data,
    }


def is_safe_vendor_text(text: str) -> bool:
    return not moderate_vendor_text(text).get("flagged", False)
