import os
from typing import Optional

from openai import OpenAI


def synthesize_text(text: str, voice: str = "alloy", model: str = "gpt-4o-mini-tts", api_key: Optional[str] = None) -> bytes:
    client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
    response = client.audio.speech.create(model=model, voice=voice, input=text, response_format="mp3")
    return response.read()
