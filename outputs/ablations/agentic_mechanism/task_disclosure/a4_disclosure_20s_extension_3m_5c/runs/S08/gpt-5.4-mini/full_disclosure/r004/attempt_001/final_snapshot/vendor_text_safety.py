import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def moderate_vendor_text(text: str, api_key: Optional[str] = None, timeout: int = 30) -> Dict[str, Any]:
    if text is None:
        text = ""
    token = api_key or os.getenv("OPENAI_API_KEY")
    if not token:
        raise ValueError("OPENAI_API_KEY is required")
    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json={"model": OPENAI_MODERATION_MODEL, "input": text},
        timeout=timeout,
    )
    response.raise_for_status()
    payload = response.json()
    result = payload["results"][0]
    categories = result.get("categories", {})
    category_scores = result.get("category_scores", {})
    flagged = bool(result.get("flagged", False))
    high_risk_categories: List[str] = [name for name, value in categories.items() if value]
    return {
        "provider": "openai",
        "model": OPENAI_MODERATION_MODEL,
        "flagged": flagged,
        "categories": categories,
        "category_scores": category_scores,
        "high_risk_categories": high_risk_categories,
        "raw": result,
    }


def is_vendor_text_safe(text: str, api_key: Optional[str] = None, timeout: int = 30) -> bool:
    return not moderate_vendor_text(text, api_key=api_key, timeout=timeout)["flagged"]


def sanitize_vendor_text(text: str, replacement: str = "[REDACTED]") -> str:
    return replacement if text else ""
