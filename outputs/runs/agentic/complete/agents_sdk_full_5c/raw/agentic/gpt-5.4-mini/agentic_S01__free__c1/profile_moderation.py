from __future__ import annotations

import os

from openai import OpenAI

# OpenAI moderation model
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))


def profile_moderation(profile_text: str) -> dict:
    result = client.moderations.create(model="omni-moderation-latest", input=profile_text)
    item = result.results[0]
    return {"flagged": item.flagged, "categories": dict(item.categories), "category_scores": dict(item.category_scores)}
