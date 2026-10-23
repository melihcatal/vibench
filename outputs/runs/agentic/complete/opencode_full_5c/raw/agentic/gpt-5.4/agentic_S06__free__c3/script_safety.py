from __future__ import annotations

import os

from openai import OpenAI


def check_script_safety(text: str) -> dict:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required for OpenAI moderation")
    client = OpenAI(api_key=api_key)
    response = client.moderations.create(model="omni-moderation-latest", input=text)
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
