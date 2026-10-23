import os
from openai import OpenAI

def check_moderation(text: str) -> dict:
    """
    Checks text for harmful content using OpenAI's Moderation API.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = client.moderations.create(
        input=text,
        model="text-moderation-latest"
    )

    result = response.results[0]
    return result.model_dump()
