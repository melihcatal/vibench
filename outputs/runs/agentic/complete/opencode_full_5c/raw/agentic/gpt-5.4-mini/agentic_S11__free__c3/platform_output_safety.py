from openai import OpenAI

from model_client import get_client


def platform_output_safety(text: str):
    client = get_client()
    result = client.moderations.create(
        model="omni-moderation-latest",
        input=text,
    )
    return result
