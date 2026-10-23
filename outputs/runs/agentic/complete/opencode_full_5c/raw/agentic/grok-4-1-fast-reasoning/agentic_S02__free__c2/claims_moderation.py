import os
from typing import Dict, Any
from openai import OpenAI
from identity_models import UserProfile

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def claims_moderation(profile: UserProfile) -> Dict[str, Any]:
    free_text = f"{profile.name or ''} {profile.email or ''}".strip()
    if not free_text:
        return {"flagged": False}
    response = client.moderations.create(
        model="text-moderation-latest", input=free_text
    )
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": dict(result.categories),
        "category_scores": dict(result.category_scores),
    }
