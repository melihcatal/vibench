import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def check_extracted_document_text(text: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json={"model": OPENAI_MODERATION_MODEL, "input": text},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    result = (data.get("results") or [{}])[0]
    categories = result.get("categories") or {}
    category_scores = result.get("category_scores") or {}
    flagged = bool(result.get("flagged"))

    unsafe_categories: List[str] = [name for name, matched in categories.items() if matched]

    return {
        "flagged": flagged,
        "unsafe_categories": unsafe_categories,
        "category_scores": category_scores,
        "raw": data,
    }


def document_is_safe(text: str, api_key: Optional[str] = None) -> bool:
    return not check_extracted_document_text(text, api_key=api_key)["flagged"]
