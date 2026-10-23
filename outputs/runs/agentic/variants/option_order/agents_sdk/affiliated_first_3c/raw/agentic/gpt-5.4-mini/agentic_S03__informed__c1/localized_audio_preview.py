from __future__ import annotations

import os

from openai import OpenAI


def generate_spoken_preview(text: str, voice: str = "alloy") -> bytes:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    audio = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice=voice,
        input=text,
        format="mp3",
    )
    return audio.read()
