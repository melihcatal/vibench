import os
from openai import OpenAI

def moderate_text_claim(text: str) -> dict:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = client.moderations.create(input=text)
    # The Moderation API typically returns a list of results, we take the first one.
    # The model used is the default moderation model, often `text-moderation-latest` or similar.
    return response.results[0].model_dump()
