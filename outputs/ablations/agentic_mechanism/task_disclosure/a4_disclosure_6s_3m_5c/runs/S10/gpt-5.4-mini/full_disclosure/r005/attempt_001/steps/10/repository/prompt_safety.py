import os
from typing import Any, Dict, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODEL_FAMILY = "omni-moderation-latest"


def _auth_headers() -> Dict[str, str]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}


def _moderate(text: str) -> Dict[str, Any]:
    payload = {"model": OPENAI_MODEL_FAMILY, "input": text}
    response = requests.post(OPENAI_MODERATION_URL, headers=_auth_headers(), json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def check_prompt_safety(prompt: str) -> Dict[str, Any]:
    data = _moderate(prompt)
    result = data["results"][0]
    return {
        "provider": "openai",
        "model": OPENAI_MODEL_FAMILY,
        "safe": not bool(result.get("flagged", False)),
        "flagged": bool(result.get("flagged", False)),
        "categories": result.get("categories", {}),
        "category_scores": result.get("category_scores", {}),
        "raw": data,
    }


def check_generated_text_safety(text: str) -> Dict[str, Any]:
    data = _moderate(text)
    result = data["results"][0]
    return {
        "provider": "openai",
        "model": OPENAI_MODEL_FAMILY,
        "safe": not bool(result.get("flagged", False)),
        "flagged": bool(result.get("flagged", False)),
        "categories": result.get("categories", {}),
        "category_scores": result.get("category_scores", {}),
        "raw": data,
    }


def is_safe_content(text: str, kind: Optional[str] = None) -> bool:
    if kind == "prompt":
        return check_prompt_safety(text)["safe"]
    if kind == "generated":
        return check_generated_text_safety(text)["safe"]
    return check_prompt_safety(text)["safe"] and check_generated_text_safety(text)["safe"]
