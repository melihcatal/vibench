from __future__ import annotations

import base64

from translation_client import OPENAI_TTS_MODEL, openai_speech
from translation_models import ensure_text


def localized_audio_preview(
    text: str, voice: str = "alloy", audio_format: str = "mp3"
) -> dict[str, str]:
    clean_text = ensure_text(text)
    audio_bytes = openai_speech(clean_text, voice=voice, audio_format=audio_format)
    return {
        "provider": "openai",
        "model": OPENAI_TTS_MODEL,
        "voice": voice,
        "format": audio_format,
        "audio_base64": base64.b64encode(audio_bytes).decode("ascii"),
    }
