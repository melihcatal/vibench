import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_DEFAULT_MODEL = "omni-moderation-latest"


def _api_key() -> str:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return key


def _extract_input(script: Any) -> str:
    if script is None:
        return ""
    if isinstance(script, str):
        return script
    if isinstance(script, dict):
        for field in ("script", "text", "content", "narration"):
            value = script.get(field)
            if isinstance(value, str):
                return value
    return str(script)


def check_script_safety(script: Any, model: Optional[str] = None, timeout: int = 30) -> Dict[str, Any]:
    payload = {
        "model": model or OPENAI_DEFAULT_MODEL,
        "input": _extract_input(script),
    }
    headers = {
        "Authorization": f"Bearer {_api_key()}",
        "Content-Type": "application/json",
    }
    response = requests.post(OPENAI_MODERATION_URL, json=payload, headers=headers, timeout=timeout)
    response.raise_for_status()
    data = response.json()
    result = (data.get("results") or [{}])[0]
    categories = result.get("categories") or {}
    category_scores = result.get("category_scores") or {}
    flagged = bool(result.get("flagged"))
    unsafe_categories = [name for name, is_flagged in categories.items() if is_flagged]
    return {
        "provider": "openai",
        "model": payload["model"],
        "flagged": flagged,
        "unsafe_categories": unsafe_categories,
        "categories": categories,
        "category_scores": category_scores,
        "raw": data,
    }
