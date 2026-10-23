import os
from typing import Optional

from openai import OpenAI


def generate_localized_audio_preview(text: str, language: str, voice: str = "alloy", model: str = "gpt-4o-mini-tts") -> bytes:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    client = OpenAI(api_key=api_key)
    response = client.audio.speech.create(model=model, voice=voice, input=text)
    return response.read()
