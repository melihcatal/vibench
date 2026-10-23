import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_localized_audio_preview(text: str, voice: str = "alloy") -> bytes:
    """
    Generates a spoken audio preview of the translated text.
    """
    response = client.audio.speech.create(model="tts-1", voice=voice, input=text)
    return response.content
