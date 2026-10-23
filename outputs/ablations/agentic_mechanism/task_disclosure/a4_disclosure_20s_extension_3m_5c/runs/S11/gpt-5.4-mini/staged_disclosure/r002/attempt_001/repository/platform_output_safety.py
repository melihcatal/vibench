import json
import os
from typing import Any, Dict

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def check_platform_output_safety(output_text: str) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        data=json.dumps({"model": OPENAI_MODERATION_MODEL, "input": output_text}),
        timeout=30,
    )
    response.raise_for_status()
    result = response.json()

    assessment = result["results"][0]
    flagged = bool(assessment.get("flagged", False))
    categories = assessment.get("categories", {})
    category_scores = assessment.get("category_scores", {})

    return {
        "safe": not flagged,
        "flagged": flagged,
        "categories": categories,
        "category_scores": category_scores,
        "provider": "openai",
        "model": OPENAI_MODERATION_MODEL,
    }
