import os
from openai import OpenAI
from typing import Dict, Any


def profile_moderation(text: str) -> Dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set")
    client = OpenAI(api_key=api_key)
    response = client.moderations.create(input=text)
    return response.results[0] if response.results else {}
