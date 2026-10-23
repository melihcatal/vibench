from __future__ import annotations

from typing import Any, Dict
import os

from openai import OpenAI


OPENAI_MODERATION_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")



def check_message_safety(payload_text: str) -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(
        model=OPENAI_MODERATION_MODEL,
        input=payload_text,
    )
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": result.categories.model_dump() if hasattr(result.categories, "model_dump") else dict(result.categories),
        "category_scores": result.category_scores.model_dump() if hasattr(result.category_scores, "model_dump") else dict(result.category_scores),
    }
