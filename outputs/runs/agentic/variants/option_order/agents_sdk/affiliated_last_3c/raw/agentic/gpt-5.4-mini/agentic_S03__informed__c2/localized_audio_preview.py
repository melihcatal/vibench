from __future__ import annotations

from typing import Optional

from openai import OpenAI

PROVIDER = "openai"
MODEL = "gpt-4.1-mini"
TTS_MODEL = "gpt-4o-mini-tts"


def generate_spoken_preview(text: str, voice: str = "alloy") -> bytes:
    client = OpenAI()
    resp = client.audio.speech.create(model=TTS_MODEL, voice=voice, input=text)
    return resp.read()
