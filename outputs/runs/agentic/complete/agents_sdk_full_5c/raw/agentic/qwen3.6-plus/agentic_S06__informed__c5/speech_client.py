"""Local configuration and client helper utilities for ElevenLabs Text-to-Speech."""

import os
from typing import Optional

from elevenlabs import ElevenLabs


ELEVENLABS_API_KEY_ENV = "ELEVENLABS_API_KEY"
DEFAULT_MODEL = "eleven_multilingual_v2"
DEFAULT_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Rachel
DEFAULT_OUTPUT_FORMAT = "mp3_44100_128"


def get_api_key() -> str:
    """Retrieve the ElevenLabs API key from environment."""
    api_key = os.environ.get(ELEVENLABS_API_KEY_ENV)
    if not api_key:
        raise ValueError(f"{ELEVENLABS_API_KEY_ENV} environment variable is required")
    return api_key


def create_elevenlabs_client(api_key: Optional[str] = None) -> ElevenLabs:
    """Create an authenticated ElevenLabs client instance."""
    key = api_key or get_api_key()
    return ElevenLabs(api_key=key)


def build_tts_request(
    text: str,
    model_id: str = DEFAULT_MODEL,
    voice_id: str = DEFAULT_VOICE_ID,
    output_format: str = DEFAULT_OUTPUT_FORMAT,
    stability: Optional[float] = None,
    similarity_boost: Optional[float] = None,
) -> dict:
    """Build a normalized request dict for ElevenLabs TTS generation."""
    voice_settings = {}
    if stability is not None:
        voice_settings["stability"] = max(0.0, min(1.0, stability))
    if similarity_boost is not None:
        voice_settings["similarity_boost"] = max(0.0, min(1.0, similarity_boost))

    request = {
        "text": text,
        "model_id": model_id,
        "voice_id": voice_id,
        "output_format": output_format,
    }
    if voice_settings:
        request["voice_settings"] = voice_settings
    return request


def normalize_voice_list_response(raw_voices: list) -> list[dict]:
    """Normalize ElevenLabs voice list response to a consistent schema."""
    normalized = []
    for voice in raw_voices:
        normalized.append({
            "voice_id": voice.voice_id,
            "name": voice.name,
            "category": getattr(voice, "category", None),
            "labels": getattr(voice, "labels", {}),
            "preview_url": getattr(voice, "preview_url", None),
        })
    return normalized


def extract_audio_bytes(response) -> bytes:
    """Extract raw audio bytes from an ElevenLabs streaming response."""
    if hasattr(response, "stream"):
        return b"".join(chunk for chunk in response.stream())
    return response
