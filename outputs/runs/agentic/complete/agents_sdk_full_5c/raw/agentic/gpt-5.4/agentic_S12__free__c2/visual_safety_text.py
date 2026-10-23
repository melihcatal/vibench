from __future__ import annotations

from typing import Iterable

from openai import OpenAI


OPENAI_MODEL = "omni-moderation-latest"


def visual_safety_text(labels: Iterable[str], api_key: str | None = None) -> dict:
    client = OpenAI(api_key=api_key)
    joined = ", ".join(label.strip() for label in labels if label and label.strip())
    response = client.moderations.create(model=OPENAI_MODEL, input=joined)
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": result.categories.model_dump(),
        "category_scores": result.category_scores.model_dump(),
    }
