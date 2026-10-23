import os
from openai import OpenAI

def moderate_profile_text(text: str) -> dict:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.moderations.create(input=text)
    # The moderation model is 'text-moderation-007' or similar under the hood
    return response.results[0].model_dump()
