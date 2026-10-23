import os
from openai import OpenAI


def moderate_transcript(text: str) -> dict:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    moderation = client.moderations.create(input=text)
    result = moderation.results[0]
    return {
        "flagged": result.flagged,
        "categories": dict(result.categories),
        "category_scores": dict(result.category_scores),
    }
