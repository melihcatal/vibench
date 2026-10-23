import os
from openai import OpenAI
from vision_client import OPENAI_API_KEY


def visual_safety_text(texts: list[str]) -> dict:
    client = OpenAI(api_key=OPENAI_API_KEY)
    full_text = " ".join(texts)
    response = client.moderations.create(input=full_text)
    result = response.results[0]
    return {
        "safe": not result.flagged,
        "categories": dict(result.categories),
        "category_scores": dict(result.category_scores),
    }
