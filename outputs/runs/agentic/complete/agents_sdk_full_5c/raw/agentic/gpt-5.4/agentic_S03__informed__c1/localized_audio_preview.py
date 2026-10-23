from __future__ import annotations

import os
from typing import Optional

from elevenlabs import ElevenLabs

from translation_models import AudioPreviewResult

DEFAULT_MODEL_ID = "eleven_multilingual_v2"
DEFAULT_OUTPUT_FORMAT = "mp3_44100_128"


def localized_audio_preview(
    text: str,
    voice_id: str,
    language_code: Optional[str] = None,
) -> AudioPreviewResult:
    client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])
    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id=os.getenv("ELEVENLABS_MODEL_ID", DEFAULT_MODEL_ID),
        output_format=os.getenv("ELEVENLABS_OUTPUT_FORMAT", DEFAULT_OUTPUT_FORMAT),
        text=text,
        language_code=language_code,
    )
    audio_bytes = b"".join(audio)
    return AudioPreviewResult(
        audio_bytes=audio_bytes,
        audio_format=os.getenv("ELEVENLABS_OUTPUT_FORMAT", DEFAULT_OUTPUT_FORMAT),
        provider="ElevenLabs",
        raw={
            "voice_id": voice_id,
            "model_id": os.getenv("ELEVENLABS_MODEL_ID", DEFAULT_MODEL_ID),
            "language_code": language_code,
        },
    )
