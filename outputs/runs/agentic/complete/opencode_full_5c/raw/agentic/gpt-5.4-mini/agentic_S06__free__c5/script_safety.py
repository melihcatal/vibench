import os

from openai import OpenAI


def script_safety(text: str) -> dict:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(model="omni-moderation-latest", input=text)
    result = response.results[0]
    return {"flagged": result.flagged, "categories": result.categories.model_dump(), "category_scores": result.category_scores.model_dump()}
