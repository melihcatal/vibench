from __future__ import annotations

import os

from openai import OpenAI


OPENAI_MODEL = "omni-moderation-latest"


def profile_moderation(profile_text: str) -> dict:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.moderations.create(model=OPENAI_MODEL, input=profile_text)
    result = response.results[0]
    return {
        "provider": "openai",
        "model": OPENAI_MODEL,
        "flagged": result.flagged,
        "categories": result.categories.model_dump(),
        "category_scores": result.category_scores.model_dump(),
    }
