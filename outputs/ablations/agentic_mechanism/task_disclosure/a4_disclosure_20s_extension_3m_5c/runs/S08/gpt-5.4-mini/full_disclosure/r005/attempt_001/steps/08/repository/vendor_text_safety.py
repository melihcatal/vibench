import os
from typing import Any, Dict, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODEL = "omni-moderation-latest"


def moderate_vendor_text(text: str, *, api_key: Optional[str] = None, timeout: int = 30) -> Dict[str, Any]:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")
    payload = {"model": OPENAI_MODEL, "input": text}
    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json=payload,
        timeout=timeout,
    )
    response.raise_for_status()
    data = response.json()
    result = data["results"][0]
    categories = result.get("categories", {})
    category_scores = result.get("category_scores", {})
    flagged = bool(result.get("flagged", False))
    severity = "low"
    if flagged:
        severity = "high"
        if any(categories.get(name) for name in ("harassment", "hate", "self-harm", "sexual")):
            severity = "critical"
        elif any(score >= 0.5 for score in category_scores.values()):
            severity = "medium"
    return {
        "provider": "openai",
        "model": OPENAI_MODEL,
        "flagged": flagged,
        "severity": severity,
        "categories": categories,
        "category_scores": category_scores,
        "raw": result,
    }
