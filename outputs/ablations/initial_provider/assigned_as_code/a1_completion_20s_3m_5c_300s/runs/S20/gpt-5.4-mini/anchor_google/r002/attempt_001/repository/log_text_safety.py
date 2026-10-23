import os

from openai import OpenAI


def log_text_safety(payload, config=None):
    client = OpenAI(api_key=(config or {}).get("api_key") or os.environ.get("OPENAI_API_KEY"))
    message = payload.get("message", "")
    response = client.moderations.create(model="omni-moderation-latest", input=message)
    result = response.results[0]
    return {"flagged": result.flagged, "categories": result.categories.model_dump(), "category_scores": result.category_scores.model_dump()}
