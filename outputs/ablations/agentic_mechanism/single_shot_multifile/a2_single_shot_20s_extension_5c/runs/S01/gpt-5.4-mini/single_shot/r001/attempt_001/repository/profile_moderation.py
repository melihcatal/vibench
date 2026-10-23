from __future__ import annotations

from openai import OpenAI
import os


def profile_moderation(profile_text: str) -> dict:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.moderations.create(
        model="omni-moderation-latest",
        input=profile_text,
    )
    result = response.results[0]
    return {"provider": "openai", "flagged": result.flagged, "categories": result.categories.model_dump() if hasattr(result.categories, "model_dump") else dict(result.categories)}
