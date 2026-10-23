from __future__ import annotations

from translation_client import OPENAI_TTS_MODEL, get_openai_client
from translation_models import AudioPreviewResult


def generate_localized_audio_preview(
    text: str,
    voice: str = "alloy",
    audio_format: str = "mp3",
) -> AudioPreviewResult:
    client = get_openai_client()
    response = client.audio.speech.create(
        model=OPENAI_TTS_MODEL,
        voice=voice,
        input=text,
        format=audio_format,
    )
    audio_bytes = response.read()
    content_type = f"audio/{audio_format}"
    return AudioPreviewResult(
        audio_bytes=audio_bytes,
        content_type=content_type,
        provider="openai",
        voice=voice,
    )
