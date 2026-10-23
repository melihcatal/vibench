import os

from openai import OpenAI


def profile_moderation(text: str):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    result = client.moderations.create(model="omni-moderation-latest", input=text)
    return result.results[0]
