from __future__ import annotations

import os
from typing import Optional

from elevenlabs import ElevenLabs

from translation_models import AudioPreviewResult


DEFAULT_ELEVENLABS_MODEL = os.getenv("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2")
DEFAULT_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb")


def generate_localized_audio_preview(
    text: str,
    voice_id: Optional[str] = None,
    model_id: Optional[str] = None,
) -> AudioPreviewResult:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("Missing ElevenLabs API key. Set ELEVENLABS_API_KEY.")
    client = ElevenLabs(api_key=api_key)
    audio = client.text_to_speech.convert(
        voice_id=voice_id or DEFAULT_VOICE_ID,
        model_id=model_id or DEFAULT_ELEVENLABS_MODEL,
        text=text,
        output_format="mp3_44100_128",
    )
    audio_bytes = b"".join(chunk for chunk in audio)
    return AudioPreviewResult(
        audio_bytes=audio_bytes,
        mime_type="audio/mpeg",
        voice=voice_id or DEFAULT_VOICE_ID,
        provider="ElevenLabs",
    )
