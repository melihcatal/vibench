from __future__ import annotations

from openai import OpenAI

from translation_client import openai_api_key
from translation_models import AudioPreviewResult


def localized_audio_preview(
    text: str, voice: str = "alloy", audio_format: str = "mp3"
) -> AudioPreviewResult:
    client = OpenAI(api_key=openai_api_key())
    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice=voice,
        input=text,
        format=audio_format,
    )
    audio_base64 = response.read().hex()
    return AudioPreviewResult(
        audio_base64=audio_base64,
        provider="openai-gpt-4o-mini-tts",
        voice=voice,
        audio_format=audio_format,
        raw={"model": "gpt-4o-mini-tts", "voice": voice, "format": audio_format},
    )
