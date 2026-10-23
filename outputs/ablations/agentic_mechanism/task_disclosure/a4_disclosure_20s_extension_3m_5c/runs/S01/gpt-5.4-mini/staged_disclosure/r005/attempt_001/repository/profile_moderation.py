import os
from typing import Any, Dict

import openai


class ProfileModerationError(Exception):
    pass


def moderate_profile_text(profile_text: str) -> Dict[str, Any]:
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.moderations.create(
        model="omni-moderation-latest",
        input=profile_text,
    )
    result = response.results[0]
    if result.flagged:
        raise ProfileModerationError("Profile text failed moderation")
    return {
        "flagged": result.flagged,
        "categories": dict(result.categories),
        "category_scores": dict(result.category_scores),
    }
