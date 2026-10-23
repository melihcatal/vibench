import os
from openai import OpenAI


def check_script_safety(script: str) -> bool:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY must be set.")
    client = OpenAI(api_key=api_key)
    response = client.moderations.create(
        input=script, model="text-moderation-3.5-2024-04-09"
    )
    return not response.results[0].flagged
