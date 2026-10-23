import os

from openai import OpenAI


def platform_output_safety(text: str) -> bool:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    result = client.moderations.create(model="omni-moderation-latest", input=text)
    return not any(item.flagged for item in result.results)
