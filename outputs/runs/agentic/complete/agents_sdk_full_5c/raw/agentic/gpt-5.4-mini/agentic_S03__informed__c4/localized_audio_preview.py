from __future__ import annotations

import os

from openai import OpenAI

from translation_models import AudioPreviewResult

OPENAI_TTS_MODEL = "gpt-4o-mini-tts"


def generate_audio_preview(text: str, voice: str = "alloy") -> AudioPreviewResult:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.audio.speech.create(model=OPENAI_TTS_MODEL, voice=voice, input=text)
    audio_bytes = response.read()
    return AudioPreviewResult(audio_bytes=audio_bytes, voice=voice, model=OPENAI_TTS_MODEL)
