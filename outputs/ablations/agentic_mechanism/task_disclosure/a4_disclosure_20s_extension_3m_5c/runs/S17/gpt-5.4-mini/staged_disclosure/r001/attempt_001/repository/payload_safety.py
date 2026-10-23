import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"


def _moderate_with_openai(text: str) -> Dict[str, Any]:
    api_key = os.getenv(OPENAI_API_KEY_ENV)
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={"input": text},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def check_decrypted_payload(payload: str) -> Dict[str, Any]:
    result = _moderate_with_openai(payload)
    output: Dict[str, Any] = {
        "safe": True,
        "provider": "openai",
        "categories": {},
        "category_scores": {},
        "raw": result,
    }
    if not result.get("results"):
        return output
    moderation = result["results"][0]
    output["categories"] = moderation.get("categories", {})
    output["category_scores"] = moderation.get("category_scores", {})
    output["safe"] = not moderation.get("flagged", False)
    return output


def is_payload_safe(payload: str) -> bool:
    return bool(check_decrypted_payload(payload)["safe"])
