from __future__ import annotations

from openai import OpenAI


OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def metric_annotation_safety(text: str) -> dict:
    client = OpenAI()
    result = client.moderations.create(model=OPENAI_MODERATION_MODEL, input=text)
    moderation = result.results[0]
    return {
        "flagged": moderation.flagged,
        "categories": moderation.categories.model_dump() if hasattr(moderation.categories, "model_dump") else dict(moderation.categories),
        "category_scores": moderation.category_scores.model_dump() if hasattr(moderation.category_scores, "model_dump") else dict(moderation.category_scores),
    }
