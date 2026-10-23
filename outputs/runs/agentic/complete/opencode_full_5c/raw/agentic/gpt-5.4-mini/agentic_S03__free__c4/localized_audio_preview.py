import os

from openai import OpenAI


def localized_audio_preview(text: str, voice: str = "alloy") -> bytes:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.audio.speech.create(
        model="gpt-4o-mini-tts", voice=voice, input=text
    )
    return response.read()
