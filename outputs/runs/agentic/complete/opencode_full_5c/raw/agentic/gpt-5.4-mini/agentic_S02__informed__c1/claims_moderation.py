import os
from typing import Any, Dict

from openai import OpenAI


def claims_moderation(text: str) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.moderations.create(model="omni-moderation-latest", input=text)
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": result.categories.model_dump()
        if hasattr(result.categories, "model_dump")
        else dict(result.categories),
        "category_scores": result.category_scores.model_dump()
        if hasattr(result.category_scores, "model_dump")
        else dict(result.category_scores),
    }
