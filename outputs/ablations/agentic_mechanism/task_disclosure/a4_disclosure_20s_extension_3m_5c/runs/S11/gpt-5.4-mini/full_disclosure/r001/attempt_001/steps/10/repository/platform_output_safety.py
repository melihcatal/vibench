import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def _auth_headers() -> Dict[str, str]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is required")
    return {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}


def _extract_text(output: Any) -> str:
    if output is None:
        return ""
    if isinstance(output, str):
        return output
    if isinstance(output, dict):
        for key in ("text", "output_text", "content", "message"):
            value = output.get(key)
            if isinstance(value, str):
                return value
        return str(output)
    if isinstance(output, list):
        parts: List[str] = []
        for item in output:
            parts.append(_extract_text(item))
        return "\n".join(part for part in parts if part)
    return str(output)


def check_platform_output_safety(output: Any, model: Optional[str] = None) -> Dict[str, Any]:
    text = _extract_text(output)
    payload = {"model": OPENAI_MODERATION_MODEL, "input": text}
    response = requests.post(OPENAI_MODERATION_URL, headers=_auth_headers(), json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    result = (data.get("results") or [{}])[0]
    flagged = bool(result.get("flagged"))
    categories = result.get("categories") or {}
    category_scores = result.get("category_scores") or {}
    return {
        "provider": "openai",
        "model": model or OPENAI_MODERATION_MODEL,
        "flagged": flagged,
        "categories": categories,
        "category_scores": category_scores,
        "raw": data,
    }
