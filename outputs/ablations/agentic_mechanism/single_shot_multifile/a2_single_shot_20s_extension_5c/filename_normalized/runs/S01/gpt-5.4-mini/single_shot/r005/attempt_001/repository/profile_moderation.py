import os
from openai import OpenAI


def profile_moderation(profile_text: str) -> dict:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    moderation = client.moderations.create(model="omni-moderation-latest", input=profile_text)
    item = moderation.results[0]
    return {"flagged": item.flagged, "categories": item.categories.model_dump(), "category_scores": item.category_scores.model_dump()}
