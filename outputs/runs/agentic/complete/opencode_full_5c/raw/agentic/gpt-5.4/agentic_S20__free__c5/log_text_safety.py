from __future__ import annotations

import os

from openai import OpenAI


def log_text_safety(message: str) -> dict:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    result = client.moderations.create(model="omni-moderation-latest", input=message)
    output = result.results[0]
    return {
        "flagged": output.flagged,
        "categories": output.categories.model_dump(),
        "category_scores": output.category_scores.model_dump(),
    }
