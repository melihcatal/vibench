from __future__ import annotations

import os

from openai import OpenAI


def claims_moderation(text: str) -> dict:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    result = client.moderations.create(model="omni-moderation-latest", input=text)
    output = result.results[0]
    return {
        "provider": "openai",
        "model": "omni-moderation-latest",
        "flagged": output.flagged,
        "categories": output.categories.model_dump(),
        "category_scores": output.category_scores.model_dump(),
    }
