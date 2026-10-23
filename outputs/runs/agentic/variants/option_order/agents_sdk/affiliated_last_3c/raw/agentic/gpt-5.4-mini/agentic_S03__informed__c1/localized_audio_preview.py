from __future__ import annotations

import os

from openai import OpenAI

from translation_models import AudioPreviewResult, normalize_text

PROVIDER_NAME = "OpenAI"
MODEL_ID = "gpt-4o-mini"


def generate_spoken_preview(text: str, voice: str = "alloy") -> AudioPreviewResult:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    normalized = normalize_text(text)
    response = client.audio.speech.create(model=MODEL_ID, voice=voice, input=normalized)
    audio_bytes = response.read()
    return AudioPreviewResult(provider=PROVIDER_NAME, audio_bytes=audio_bytes, content_type="audio/mpeg")
