import os
from openai import OpenAI


def profile_moderation(text: str) -> dict:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(input=text)
    return {
        "flagged": response.results[0].flagged,
        "categories": response.results[0].categories,
        "category_scores": response.results[0].category_scores,
    }
