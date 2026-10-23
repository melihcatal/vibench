import os

from openai import OpenAI


def corpus_safety(text: str):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(model="omni-moderation-latest", input=text)
    return response.results[0].model_dump() if hasattr(response.results[0], "model_dump") else response.results[0]
