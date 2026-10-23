from __future__ import annotations

from typing import Any, Dict

from openai import OpenAI


def check_live_caption_safety(text: str) -> Dict[str, Any]:
    client = OpenAI(api_key=None)
    response = client.moderations.create(
        model="omni-moderation-latest",
        input=text,
    )
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": result.categories.model_dump(),
        "category_scores": result.category_scores.model_dump(),
    }
