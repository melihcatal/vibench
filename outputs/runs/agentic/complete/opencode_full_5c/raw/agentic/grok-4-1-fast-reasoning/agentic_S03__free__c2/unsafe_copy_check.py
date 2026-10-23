import os
from openai import OpenAI


def is_unsafe_copy(text: str) -> bool:
    """
    Checks localized copy for unsafe content using OpenAI Moderation.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    if not text.strip():
        return False
    response = client.moderations.create(input=text, model="text-moderation-latest")
    return response.results[0].flagged
