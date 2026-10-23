import os
from typing import Any, Dict

from openai import OpenAI


def profile_moderation(event: Dict[str, Any]) -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))
    text = str(event.get("profile_text", "")).strip()
    model = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")
    response = client.moderations.create(model=model, input=text)
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": result.categories.model_dump(),
        "category_scores": result.category_scores.model_dump(),
    }
