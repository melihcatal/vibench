import json
import os
from typing import Any, Dict, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODEL = "omni-moderation-latest"


def moderate_vendor_text(text: str, *, api_key: Optional[str] = None, timeout: int = 30) -> Dict[str, Any]:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is required")
    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        data=json.dumps({"model": OPENAI_MODEL, "input": text}),
        timeout=timeout,
    )
    response.raise_for_status()
    payload = response.json()
    result = payload["results"][0]
    return {
        "flagged": bool(result.get("flagged", False)),
        "categories": result.get("categories", {}),
        "category_scores": result.get("category_scores", {}),
        "raw": payload,
    }


def moderate_vendor_note(note: str, *, api_key: Optional[str] = None, timeout: int = 30) -> bool:
    return moderate_vendor_text(note, api_key=api_key, timeout=timeout)["flagged"]
