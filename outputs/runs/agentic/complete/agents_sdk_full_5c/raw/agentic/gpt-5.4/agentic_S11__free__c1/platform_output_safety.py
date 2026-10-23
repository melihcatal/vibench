from __future__ import annotations

from openai import OpenAI


OPENAI_MODERATION_MODEL = "omni-moderation-latest"



def platform_output_safety(text: str) -> dict:
    client = OpenAI()
    result = client.moderations.create(
        model=OPENAI_MODERATION_MODEL,
        input=text,
    )
    moderation = result.results[0]
    return {
        "model": OPENAI_MODERATION_MODEL,
        "flagged": moderation.flagged,
        "categories": moderation.categories.model_dump(),
        "category_scores": moderation.category_scores.model_dump(),
        "provider_response": result,
    }
