from __future__ import annotations

import os
from typing import Any

from elevenlabs.client import ElevenLabs


DEFAULT_TTS_MODEL_ID = os.getenv("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2")
DEFAULT_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb")


def get_elevenlabs_client(api_key: str | None = None) -> ElevenLabs:
    key = api_key or os.getenv("ELEVENLABS_API_KEY")
    if not key:
        raise ValueError("ELEVENLABS_API_KEY is required")
    return ElevenLabs(api_key=key)


def get_tts_defaults() -> dict[str, str]:
    return {
        "model_id": DEFAULT_TTS_MODEL_ID,
        "voice_id": DEFAULT_VOICE_ID,
    }


def iter_audio_chunks(audio: Any) -> bytes:
    if isinstance(audio, (bytes, bytearray)):
        return bytes(audio)
    if hasattr(audio, "__iter__"):
        return b"".join(bytes(chunk) for chunk in audio if chunk)
    raise TypeError("Unsupported ElevenLabs audio stream")
