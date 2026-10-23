import openai
import os


def check_payload_safety(payload: str) -> dict:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required.")
    client = openai.OpenAI(api_key=api_key)
    moderation = client.moderations.create(
        input=payload, model="text-moderation-latest"
    )
    return moderation.results[0]
