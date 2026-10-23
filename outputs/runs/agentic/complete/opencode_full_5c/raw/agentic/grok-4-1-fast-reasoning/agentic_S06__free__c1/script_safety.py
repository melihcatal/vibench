import os
from openai import OpenAI


def check_safety(text: str) -> dict:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(input=text)
    return response.results[0].model_dump()
