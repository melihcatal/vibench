from __future__ import annotations

from typing import Optional

from openai import OpenAI

from model_client import DEFAULT_TTS_MODEL, get_client


def platform_brief_audio(text: str, voice: str = "alloy", client: Optional[OpenAI] = None) -> bytes:
    client = client or get_client()
    audio = client.audio.speech.create(model=DEFAULT_TTS_MODEL, voice=voice, input=text)
    return audio.read()
