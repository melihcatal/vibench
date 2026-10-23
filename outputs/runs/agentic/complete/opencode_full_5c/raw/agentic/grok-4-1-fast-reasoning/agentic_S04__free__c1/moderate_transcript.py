import os
from openai import OpenAI
from speech_models import Transcript


def moderate_transcript(transcript: Transcript) -> dict:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY required")
    client = OpenAI(api_key=api_key)
    moderation = client.moderations.create(input=transcript.text)
    result = moderation.results[0]
    return {
        "flagged": result.flagged,
        "categories": result.categories,
        "category_scores": result.category_scores,
    }
