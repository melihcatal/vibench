from __future__ import annotations

from typing import Any, Dict

import requests

from document_client import get_openai_headers


OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def vendor_text_safety(vendor_notes: str) -> Dict[str, Any]:
    response = requests.post(
        "https://api.openai.com/v1/moderations",
        headers=get_openai_headers(),
        json={"model": OPENAI_MODERATION_MODEL, "input": vendor_notes},
        timeout=30,
    )
    response.raise_for_status()
    result = response.json()["results"][0]
    return {
        "flagged": result.get("flagged", False),
        "categories": result.get("categories", {}),
        "category_scores": result.get("category_scores", {}),
        "model": OPENAI_MODERATION_MODEL,
        "provider": "openai",
    }
