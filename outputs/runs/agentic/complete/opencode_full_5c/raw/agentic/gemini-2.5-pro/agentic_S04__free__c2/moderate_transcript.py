import os
import openai
from speech_models import TranscriptionUtterance


def moderate_transcript(segments: list[TranscriptionUtterance]) -> list[dict]:
    """
    Moderates transcript text using OpenAI's Moderation API.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    client = openai.OpenAI()

    moderation_results = []
    for segment in segments:
        response = client.moderations.create(
            input=segment.text, model="text-moderation-latest"
        )
        moderation_results.append(response.results[0].model_dump())
    return moderation_results
