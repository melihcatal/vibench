from __future__ import annotations

import os

from openai import OpenAI


client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def moderate_claims_text(text: str) -> dict:
    moderation = client.moderations.create(
        model="omni-moderation-latest",
        input=text,
    )
    result = moderation.results[0]
    return {"flagged": result.flagged, "categories": result.categories, "category_scores": result.category_scores}
