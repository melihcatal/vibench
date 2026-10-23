import os
from openai import OpenAI


def profile_moderation(profile_text: str) -> bool:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(input=profile_text)
    result = response.results[0]
    flagged = any(score > 0.5 for score in result.category_scores.values())
    return not flagged
