from __future__ import annotations

import os
from typing import Any, Dict

from openai import OpenAI


OPENAI_MODERATION_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


def log_text_safety(message: str) -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    result = client.moderations.create(model=OPENAI_MODERATION_MODEL, input=message)
    item = result.results[0]
    return {
        "model": OPENAI_MODERATION_MODEL,
        "flagged": item.flagged,
        "categories": item.categories.model_dump(),
        "category_scores": item.category_scores.model_dump(),
    }
