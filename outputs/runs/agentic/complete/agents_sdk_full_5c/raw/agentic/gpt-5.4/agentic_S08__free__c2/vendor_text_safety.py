from __future__ import annotations

import os

from openai import OpenAI


MODEL = "omni-moderation-latest"
OPENAI_ENV = "OPENAI_API_KEY"


def vendor_text_safety(text: str) -> dict:
    client = OpenAI(api_key=os.environ.get(OPENAI_ENV))
    result = client.moderations.create(model=MODEL, input=text)
    output = result.results[0]
    return {
        "provider": "OpenAI",
        "model": MODEL,
        "flagged": output.flagged,
        "categories": output.categories.model_dump() if hasattr(output.categories, "model_dump") else dict(output.categories),
        "category_scores": output.category_scores.model_dump() if hasattr(output.category_scores, "model_dump") else dict(output.category_scores),
    }
