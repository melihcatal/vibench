import os
import openai


def moderate_transcript_text(text: str) -> dict:
    """
    Moderate transcript text before publishing using OpenAI's Moderation API.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY environment variable not set.")

    client = openai.OpenAI(api_key=api_key)

    response = client.moderations.create(input=text, model="text-moderation-latest")

    return response.results[0].model_dump()
