import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def moderate_transcript(text: str) -> dict:
    """
    Moderate transcript text using OpenAI Moderation API.
    Returns the moderation result.
    """
    client = openai.OpenAI(api_key=openai.api_key)
    response = client.moderations.create(
        input=text,
        model="text-moderation-3.5-stable"
    )
    return response.results[0].model_dump()