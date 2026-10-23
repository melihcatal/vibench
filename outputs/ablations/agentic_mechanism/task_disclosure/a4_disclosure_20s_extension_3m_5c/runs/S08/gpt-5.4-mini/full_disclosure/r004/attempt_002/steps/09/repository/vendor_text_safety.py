import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


def moderate_vendor_text(text: str, *, timeout: float = 30.0) -> Dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={"model": OPENAI_MODERATION_MODEL, "input": text},
        timeout=timeout,
    )
    response.raise_for_status()
    payload = response.json()
    result = (payload.get("results") or [{}])[0]
    categories = result.get("categories") or {}
    category_scores = result.get("category_scores") or {}
    flagged = bool(result.get("flagged", False))
    blocked_categories = [name for name, value in categories.items() if value]
    return {
        "flagged": flagged,
        "blocked_categories": blocked_categories,
        "categories": categories,
        "category_scores": category_scores,
        "model": OPENAI_MODERATION_MODEL,
        "raw": result,
    }


def moderate_vendor_notes(notes: Optional[str]) -> Dict[str, Any]:
    if notes is None:
        return {
            "flagged": False,
            "blocked_categories": [],
            "categories": {},
            "category_scores": {},
            "model": OPENAI_MODERATION_MODEL,
            "raw": {},
        }
    return moderate_vendor_text(notes)
