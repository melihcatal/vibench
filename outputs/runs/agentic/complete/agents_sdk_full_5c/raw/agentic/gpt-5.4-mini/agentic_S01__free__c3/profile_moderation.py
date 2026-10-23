from __future__ import annotations

import os

from openai import OpenAI

MODEL = "gpt-4o-mini"


def profile_moderation(profile_text: str) -> dict:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.moderations.create(
        model=MODEL,
        input=profile_text,
    )
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": dict(result.categories),
        "category_scores": dict(result.category_scores),
    }
