import json
import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def _get_api_key(api_key: Optional[str] = None) -> str:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")
    return key


def moderate_vendor_text(text: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    key = _get_api_key(api_key)
    payload = {"model": OPENAI_MODERATION_MODEL, "input": text}
    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        data=json.dumps(payload),
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    result = data["results"][0]
    return {
        "flagged": bool(result.get("flagged", False)),
        "categories": result.get("categories", {}),
        "category_scores": result.get("category_scores", {}),
        "model": data.get("model", OPENAI_MODERATION_MODEL),
    }


def moderate_vendor_notes(notes: List[str], api_key: Optional[str] = None) -> Dict[str, Any]:
    assessments = [moderate_vendor_text(note, api_key=api_key) for note in notes]
    return {
        "flagged": any(item["flagged"] for item in assessments),
        "assessments": assessments,
    }
