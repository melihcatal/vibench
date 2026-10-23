import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def moderate_transcript(text: str, model: str = OPENAI_MODERATION_MODEL, api_key: Optional[str] = None) -> Dict[str, Any]:
    if text is None:
        raise ValueError("text is required")
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is required")
    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json={"model": model, "input": text},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    result = data["results"][0]
    categories = result.get("categories", {})
    category_scores = result.get("category_scores", {})
    flagged = bool(result.get("flagged", False))
    violations: List[str] = [name for name, active in categories.items() if active]
    return {
        "provider": "openai",
        "model": model,
        "flagged": flagged,
        "violations": violations,
        "categories": categories,
        "category_scores": category_scores,
        "raw": data,
    }
