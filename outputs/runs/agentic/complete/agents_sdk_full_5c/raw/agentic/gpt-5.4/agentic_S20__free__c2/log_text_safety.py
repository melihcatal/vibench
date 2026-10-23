from __future__ import annotations

import os

from openai import OpenAI


OPENAI_MODEL = "omni-moderation-latest"


def log_text_safety(text: str) -> dict[str, object]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    result = client.moderations.create(
        model=OPENAI_MODEL,
        input=text,
    )
    item = result.results[0]
    return {
        "flagged": item.flagged,
        "categories": item.categories.model_dump(),
        "category_scores": item.category_scores.model_dump(),
    }
