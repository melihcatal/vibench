import os

import openai


def moderate_claims(text: str) -> dict:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    result = client.moderations.create(model="omni-moderation-latest", input=text)
    return result.model_dump()
