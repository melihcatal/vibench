import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_BASE_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODEL_HINT = "omni-moderation-latest"


class VendorTextSafetyError(Exception):
    pass


def _get_api_key(api_key: Optional[str] = None) -> str:
    key = api_key or os.getenv(OPENAI_API_KEY_ENV)
    if not key:
        raise VendorTextSafetyError(f"Missing {OPENAI_API_KEY_ENV}")
    return key


def moderate_vendor_text(text: str, api_key: Optional[str] = None, timeout: int = 30) -> Dict[str, Any]:
    if text is None:
        text = ""
    payload = {"model": OPENAI_MODEL_HINT, "input": text}
    headers = {
        "Authorization": f"Bearer {_get_api_key(api_key)}",
        "Content-Type": "application/json",
    }
    response = requests.post(OPENAI_BASE_URL, json=payload, headers=headers, timeout=timeout)
    if response.status_code >= 400:
        raise VendorTextSafetyError(f"OpenAI moderation request failed: {response.status_code} {response.text}")
    data = response.json()
    results = data.get("results") or []
    if not results:
        raise VendorTextSafetyError("OpenAI moderation returned no results")
    result = results[0]
    categories = result.get("categories") or {}
    category_scores = result.get("category_scores") or {}
    flagged = bool(result.get("flagged"))
    return {
        "provider": "openai",
        "model": OPENAI_MODEL_HINT,
        "flagged": flagged,
        "categories": categories,
        "category_scores": category_scores,
        "raw": result,
    }


def is_vendor_text_safe(text: str, api_key: Optional[str] = None, timeout: int = 30) -> bool:
    return not moderate_vendor_text(text, api_key=api_key, timeout=timeout)["flagged"]
