import os
from typing import Any, Dict, Optional

import httpx


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_DEFAULT_MODEL = "omni-moderation-latest"


def _api_key(api_key: Optional[str] = None) -> str:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")
    return key


def check_platform_output_safety(
    output: str,
    api_key: Optional[str] = None,
    model: str = OPENAI_DEFAULT_MODEL,
) -> Dict[str, Any]:
    headers = {
        "Authorization": f"Bearer {_api_key(api_key)}",
        "Content-Type": "application/json",
    }
    payload = {"model": model, "input": output}
    response = httpx.post(OPENAI_MODERATION_URL, headers=headers, json=payload, timeout=30.0)
    response.raise_for_status()
    data = response.json()
    result = data.get("results", [{}])[0]
    categories = result.get("categories", {})
    category_scores = result.get("category_scores", {})
    flagged = bool(result.get("flagged", False))
    unsafe_categories = [name for name, is_unsafe in categories.items() if is_unsafe]
    return {
        "provider": "openai",
        "model": model,
        "flagged": flagged,
        "unsafe_categories": unsafe_categories,
        "category_scores": category_scores,
        "raw_response": data,
    }
