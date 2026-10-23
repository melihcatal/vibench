import os
from typing import Any, Dict

from openai import OpenAI


class ProfileModerationError(Exception):
    pass


def moderate_profile_text(profile_text: str) -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(
        model="omni-moderation-latest",
        input=profile_text,
    )
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": result.categories.model_dump() if hasattr(result.categories, "model_dump") else dict(result.categories),
        "category_scores": result.category_scores.model_dump() if hasattr(result.category_scores, "model_dump") else dict(result.category_scores),
    }


def is_profile_approved(profile_text: str) -> bool:
    return not moderate_profile_text(profile_text)["flagged"]
