from __future__ import annotations

from typing import Any, Dict

from openai import OpenAI


OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def check_script_safety(text: str, api_key: str) -> Dict[str, Any]:
    client = OpenAI(api_key=api_key)
    result = client.moderations.create(model=OPENAI_MODERATION_MODEL, input=text)
    item = result.results[0]
    return {
        "provider": "OpenAI",
        "model": OPENAI_MODERATION_MODEL,
        "flagged": item.flagged,
        "categories": item.categories.model_dump(),
        "category_scores": item.category_scores.model_dump(),
    }
