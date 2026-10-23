from __future__ import annotations

import os

from openai import OpenAI


def log_text_safety(message: str, model: str = "omni-moderation-latest") -> dict:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.moderations.create(model=model, input=message)
    result = response.results[0]
    return {
        "provider": "OpenAI",
        "model": model,
        "flagged": result.flagged,
        "categories": result.categories.model_dump(),
        "category_scores": result.category_scores.model_dump(),
    }
