from __future__ import annotations

import os

from openai import OpenAI


OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def moderate_transcript(text: str) -> dict[str, object]:
    if not os.getenv(OPENAI_API_KEY_ENV):
        raise RuntimeError(
            f"Missing required environment variable: {OPENAI_API_KEY_ENV}"
        )
    client = OpenAI()
    response = client.moderations.create(model=OPENAI_MODERATION_MODEL, input=text)
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": result.categories.model_dump(),
        "category_scores": result.category_scores.model_dump(),
        "provider": "openai",
        "model": OPENAI_MODERATION_MODEL,
    }
