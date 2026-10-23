import os
from openai import OpenAI


def vendor_text_safety(payload, config=None):
    client = OpenAI(api_key=(config or {}).get("api_key") or os.environ.get("OPENAI_API_KEY"))
    moderation = client.moderations.create(model="omni-moderation-latest", input=payload.get("text", ""))
    result = moderation.results[0]
    return {"flagged": result.flagged, "categories": result.categories.model_dump(), "category_scores": result.category_scores.model_dump()}
