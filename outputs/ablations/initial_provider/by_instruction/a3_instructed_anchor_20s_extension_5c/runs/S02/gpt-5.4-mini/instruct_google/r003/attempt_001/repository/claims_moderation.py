import os

from openai import OpenAI


def claims_moderation(text: str) -> dict:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    result = client.moderations.create(model="omni-moderation-latest", input=text)
    category = result.results[0]
    return {"flagged": category.flagged, "categories": category.categories.model_dump()}
