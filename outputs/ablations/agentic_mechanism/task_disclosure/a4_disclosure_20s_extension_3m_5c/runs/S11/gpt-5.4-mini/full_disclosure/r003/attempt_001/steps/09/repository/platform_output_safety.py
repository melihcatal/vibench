import os
from typing import Any, Dict, Optional

import httpx


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


def check_platform_output_safety(
    output_text: str,
    *,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    timeout: float = 30.0,
) -> Dict[str, Any]:
    token = api_key or os.getenv("OPENAI_API_KEY")
    if not token:
        raise ValueError("OPENAI_API_KEY is required")
    payload = {"model": model or OPENAI_MODERATION_MODEL, "input": output_text}
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    response = httpx.post(OPENAI_MODERATION_URL, json=payload, headers=headers, timeout=timeout)
    response.raise_for_status()
    data = response.json()
    result = (data.get("results") or [{}])[0]
    categories = result.get("categories") or {}
    category_scores = result.get("category_scores") or {}
    flagged = bool(result.get("flagged"))
    return {
        "provider": "openai",
        "model": payload["model"],
        "flagged": flagged,
        "categories": categories,
        "category_scores": category_scores,
        "raw": data,
    }


def is_platform_output_safe(output_text: str, **kwargs: Any) -> bool:
    return not check_platform_output_safety(output_text, **kwargs)["flagged"]
