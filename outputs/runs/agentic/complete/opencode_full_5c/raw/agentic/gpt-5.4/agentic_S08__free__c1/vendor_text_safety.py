from __future__ import annotations

import os
from typing import Any, Dict

from openai import OpenAI


OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def vendor_text_safety(text: str) -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    result = client.moderations.create(model=OPENAI_MODERATION_MODEL, input=text)
    payload = result.results[0]
    return {
        "provider": "openai",
        "model": OPENAI_MODERATION_MODEL,
        "flagged": payload.flagged,
        "categories": payload.categories.model_dump(),
        "category_scores": payload.category_scores.model_dump(),
    }
