from __future__ import annotations

import os
from typing import Any, Dict

from openai import OpenAI


OPENAI_MODERATION_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


def check_message_safety(text: str) -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(
        model=OPENAI_MODERATION_MODEL,
        input=text,
    )
    result = response.results[0]
    categories = {name: bool(value) for name, value in result.categories.model_dump().items()}
    scores = result.category_scores.model_dump()
    return {
        "provider": "openai",
        "model": OPENAI_MODERATION_MODEL,
        "flagged": bool(result.flagged),
        "categories": categories,
        "category_scores": scores,
    }
