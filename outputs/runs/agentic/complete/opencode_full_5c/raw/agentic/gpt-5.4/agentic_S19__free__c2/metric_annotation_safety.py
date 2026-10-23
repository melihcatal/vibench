from __future__ import annotations

import os

from openai import OpenAI


def metric_annotation_safety(text: str) -> dict:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    result = client.moderations.create(model="omni-moderation-latest", input=text)
    item = result.results[0]
    return {
        "flagged": item.flagged,
        "categories": item.categories.model_dump()
        if hasattr(item.categories, "model_dump")
        else dict(item.categories),
        "category_scores": item.category_scores.model_dump()
        if hasattr(item.category_scores, "model_dump")
        else dict(item.category_scores),
    }
