import os
from openai import OpenAI

def check_text_safety(text_content: str) -> dict:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    response = client.moderations.create(
        input=text_content,
        model="text-moderation-latest"
    )

    moderation_result = response.results[0]
    return moderation_result.model_dump()
