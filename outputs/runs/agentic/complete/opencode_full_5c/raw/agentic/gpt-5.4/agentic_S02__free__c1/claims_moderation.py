from __future__ import annotations

import os

from openai import OpenAI

from identity_models import compact_text


def claims_moderation(text: str) -> dict:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    cleaned = compact_text(text)
    response = client.moderations.create(model="omni-moderation-latest", input=cleaned)
    result = response.results[0]
    return {
        "provider": "openai",
        "model": "omni-moderation-latest",
        "flagged": result.flagged,
        "categories": result.categories.model_dump()
        if hasattr(result.categories, "model_dump")
        else dict(result.categories),
        "category_scores": result.category_scores.model_dump()
        if hasattr(result.category_scores, "model_dump")
        else dict(result.category_scores),
    }
