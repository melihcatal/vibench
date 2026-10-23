import json
import os
from typing import Any, Dict, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"


class ModerationError(Exception):
    pass


def moderate_profile_text(profile_text: str, threshold: float = 0.5) -> Dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ModerationError("OPENAI_API_KEY is required")

    payload = {"model": "omni-moderation-latest", "input": profile_text}
    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        data=json.dumps(payload),
        timeout=30,
    )

    if response.status_code != 200:
        raise ModerationError(f"OpenAI moderation API error: {response.status_code} {response.text}")

    data = response.json()
    result = data["results"][0]
    categories = result.get("categories", {})
    category_scores = result.get("category_scores", {})
    flagged = bool(result.get("flagged", False))

    highest_score = max(category_scores.values(), default=0.0)
    is_allowed = (not flagged) and highest_score < threshold

    return {
        "allowed": is_allowed,
        "flagged": flagged,
        "categories": categories,
        "category_scores": category_scores,
        "provider": "openai",
        "model": "omni-moderation-latest",
    }


def moderate_profile(profile_text: str) -> bool:
    return moderate_profile_text(profile_text)["allowed"]
