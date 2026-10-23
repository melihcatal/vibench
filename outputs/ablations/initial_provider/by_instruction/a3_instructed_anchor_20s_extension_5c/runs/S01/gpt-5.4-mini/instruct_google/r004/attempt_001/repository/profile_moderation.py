from typing import Any, Dict

from openai import OpenAI


def profile_moderation(text: str) -> Dict[str, Any]:
    client = OpenAI()
    result = client.moderations.create(model="omni-moderation-latest", input=text)
    item = result.results[0]
    return {"flagged": item.flagged, "categories": item.categories.model_dump(), "category_scores": item.category_scores.model_dump()}
