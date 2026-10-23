import os

from openai import OpenAI


def vendor_text_safety(text):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(model="omni-moderation-latest", input=text)
    return {"provider": "openai", "flagged": response.results[0].flagged}
