import os
from openai import OpenAI

def profile_moderation(text: str) -> bool:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Missing OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    response = client.moderations.create(input=text)
    return not response.results[0].flagged