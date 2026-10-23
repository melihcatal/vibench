import os
from openai import OpenAI


def moderate_transcript_text(text: str) -> dict:
    """
    Moderates transcript text before publishing using OpenAI's Moderation API.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.moderations.create(input=text)
    return response.results[0].model_dump()
