import os
from openai import OpenAI


def visual_safety_text(labels: list[str]) -> dict:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    text = " ".join(labels)
    response = client.moderations.create(
        model="text-moderation-latest",
        input=text,
    )
    return response.results[0]
