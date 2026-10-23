from __future__ import annotations

from typing import Dict

from openai import OpenAI


TTS_MODEL = "gpt-4o-mini-tts"


def generate_spoken_preview(text: str, voice: str = "alloy") -> Dict[str, str]:
    client = OpenAI()
    response = client.audio.speech.create(model=TTS_MODEL, voice=voice, input=text)
    audio_bytes = response.read()
    return {"provider": "openai", "model": TTS_MODEL, "voice": voice, "audio_bytes": str(len(audio_bytes))}
