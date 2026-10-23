import os
from dataclasses import dataclass

from openai import OpenAI


@dataclass(frozen=True)
class AudioPreview:
    text: str
    voice: str


def generate_audio_preview(text: str, voice: str = "alloy") -> AudioPreview:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    client.audio.speech.create(model="gpt-4o-mini-tts", voice=voice, input=text)
    return AudioPreview(text=text, voice=voice)
