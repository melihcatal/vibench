import os
from openai import OpenAI


def check_safety(script: str) -> dict:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(input=script)
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": dict(result.categories),
        "category_scores": {k: float(v) for k, v in result.category_scores.items()},
    }
