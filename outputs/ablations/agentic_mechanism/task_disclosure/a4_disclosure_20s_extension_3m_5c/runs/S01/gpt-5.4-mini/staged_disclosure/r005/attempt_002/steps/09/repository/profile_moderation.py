import os
from typing import Any, Dict

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def moderate_profile_text(profile_text: str) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODERATION_MODEL,
            "input": profile_text,
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()

    result = data.get("output", [{}])[0].get("content", [{}])[0].get("result", {})
    flagged = bool(result.get("flagged", False))
    categories = result.get("categories", {})
    category_scores = result.get("category_scores", {})

    return {
        "flagged": flagged,
        "categories": categories,
        "category_scores": category_scores,
        "raw_response": data,
    }


def is_profile_approved(profile_text: str) -> bool:
    return not moderate_profile_text(profile_text)["flagged"]
