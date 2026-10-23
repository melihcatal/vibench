import os

from openai import OpenAI


def script_safety(payload, config=None):
    data = dict(payload or {})
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(input=data["text"])
    result = response.results[0]
    return {"flagged": result.flagged, "categories": dict(result.categories), "category_scores": dict(result.category_scores)}
