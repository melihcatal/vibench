from __future__ import annotations

from openai import OpenAI


OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def log_text_safety(text: str):
    client = OpenAI()
    result = client.moderations.create(
        model=OPENAI_MODERATION_MODEL,
        input=text,
    )
    output = result.results[0]
    return {
        "flagged": output.flagged,
        "categories": output.categories.model_dump() if hasattr(output.categories, "model_dump") else dict(output.categories),
        "category_scores": output.category_scores.model_dump() if hasattr(output.category_scores, "model_dump") else dict(output.category_scores),
    }
