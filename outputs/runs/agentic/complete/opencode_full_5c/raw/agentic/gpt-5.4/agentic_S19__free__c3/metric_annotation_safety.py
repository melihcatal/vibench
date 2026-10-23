from __future__ import annotations

from openai import OpenAI


def metric_annotation_safety(text: str) -> dict:
    client = OpenAI()
    response = client.moderations.create(model="omni-moderation-latest", input=text)
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": result.categories.model_dump(),
        "category_scores": result.category_scores.model_dump(),
    }
