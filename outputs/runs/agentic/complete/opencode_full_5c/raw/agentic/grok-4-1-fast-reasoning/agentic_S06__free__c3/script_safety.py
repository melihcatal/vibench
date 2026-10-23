import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def check_script_safety(script: str) -> dict:
    response = client.moderations.create(
        input=script,
        model="text-moderation-latest",
    )
    return response.results[0]
