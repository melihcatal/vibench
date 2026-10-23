from __future__ import annotations

from openai import OpenAI


OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def log_text_safety(message: str) -> dict:
    client = OpenAI()
    response = client.moderations.create(
        model=OPENAI_MODERATION_MODEL,
        input=message,
    )
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": result.categories.model_dump() if hasattr(result.categories, "model_dump") else dict(result.categories),
        "category_scores": result.category_scores.model_dump() if hasattr(result.category_scores, "model_dump") else dict(result.category_scores),
    }
