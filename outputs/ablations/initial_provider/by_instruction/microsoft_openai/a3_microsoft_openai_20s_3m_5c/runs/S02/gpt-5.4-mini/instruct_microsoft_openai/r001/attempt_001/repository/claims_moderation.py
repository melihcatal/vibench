import os

from openai import OpenAI


def moderate_claim_text(text: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"))
    response = client.moderations.create(model="omni-moderation-latest", input=text)
    return str(response.results[0].flagged)
