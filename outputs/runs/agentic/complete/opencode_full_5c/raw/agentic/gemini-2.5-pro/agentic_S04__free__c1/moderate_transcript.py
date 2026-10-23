import os
import openai


def moderate_transcript(transcript_text: str) -> dict:
    """
    Moderates transcript text before publishing using OpenAI's Moderation API.
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    response = openai.Moderation.create(
        input=transcript_text, model="text-moderation-latest"
    )
    return response["results"][0]
