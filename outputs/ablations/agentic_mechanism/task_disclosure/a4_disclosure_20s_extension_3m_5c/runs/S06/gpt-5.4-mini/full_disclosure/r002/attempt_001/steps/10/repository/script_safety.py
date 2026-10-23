import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def check_script_safety(script: str, categories: Optional[List[str]] = None) -> Dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload: Dict[str, Any] = {"model": OPENAI_MODERATION_MODEL, "input": script}
    if categories:
        payload["categories"] = categories

    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    result = response.json()
    output = result["results"][0]
    return {
        "flagged": bool(output.get("flagged", False)),
        "categories": output.get("categories", {}),
        "category_scores": output.get("category_scores", {}),
        "raw": result,
    }
