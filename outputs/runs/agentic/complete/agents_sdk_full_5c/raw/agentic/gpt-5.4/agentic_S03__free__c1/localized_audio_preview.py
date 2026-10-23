from __future__ import annotations

import requests

from translation_client import (
    DEFAULT_ELEVENLABS_MODEL,
    DEFAULT_ELEVENLABS_VOICE_ID,
    get_elevenlabs_headers,
)
from translation_models import AudioPreviewResult


ELEVENLABS_BASE_URL = "https://api.elevenlabs.io/v1"


def localized_audio_preview(translated_text: str) -> AudioPreviewResult:
    response = requests.post(
        f"{ELEVENLABS_BASE_URL}/text-to-speech/{DEFAULT_ELEVENLABS_VOICE_ID}",
        headers=get_elevenlabs_headers(),
        json={
            "text": translated_text,
            "model_id": DEFAULT_ELEVENLABS_MODEL,
            "voice_settings": {"stability": 0.4, "similarity_boost": 0.8},
        },
        timeout=60,
    )
    response.raise_for_status()
    return AudioPreviewResult(audio_bytes=response.content, content_type=response.headers.get("Content-Type", "audio/mpeg"))
