from model_client import get_llm_client, get_model_id
from typing import Optional


def generate_spoken_brief(
    text: str, model_family: str = "tts-1", voice: str = "alloy"
) -> bytes:
    client = get_llm_client()
    model = get_model_id(model_family)
    speech_response = client.audio.speech.create(model=model, voice=voice, input=text)
    return speech_response.content
