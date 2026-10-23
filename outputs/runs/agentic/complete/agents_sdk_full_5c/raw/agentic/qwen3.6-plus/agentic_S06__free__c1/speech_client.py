"""
speech_client.py - Local configuration and client helper utilities for Text-to-Speech.
Uses ElevenLabs as the concrete TTS provider.
"""

import os
from typing import Optional

import httpx
from elevenlabs import ElevenLabs


ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_BASE_URL = "https://api.elevenlabs.io"


def get_elevenlabs_client(
    api_key: Optional[str] = None,
    timeout: float = 30.0,
) -> ElevenLabs:
    """Create an authenticated ElevenLabs TTS client.

    Args:
        api_key: ElevenLabs API key. Falls back to ELEVENLABS_API_KEY env var.
        timeout: Request timeout in seconds.

    Returns:
        Configured ElevenLabs SDK client instance.
    """
    key = api_key or ELEVENLABS_API_KEY
    if not key:
        raise ValueError(
            "ELEVENLABS_API_KEY environment variable must be set "
            "or an explicit api_key must be provided."
        )
    client = ElevenLabs(
        api_key=key,
        timeout=httpx.Timeout(timeout=timeout),
    )
    return client


def get_api_base_url() -> str:
    """Return the ElevenLabs API base URL."""
    return ELEVENLABS_BASE_URL


def build_tts_headers(api_key: Optional[str] = None) -> dict:
    """Build HTTP headers for direct ElevenLabs REST calls.

    Args:
        api_key: API key for authorization.

    Returns:
        Headers dict with xi-api-key and content-type.
    """
    key = api_key or ELEVENLABS_API_KEY
    return {
        "xi-api-key": key,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }


def validate_audio_format(output_format: str) -> str:
    """Validate and normalize an ElevenLabs audio output format.

    Supported formats: mp3_22050_32, mp3_44100_32, mp3_44100_64,
                       mp3_44100_128, pcm_16000, pcm_22050,
                       ulaw_8000, alaw_8000

    Args:
        output_format: Desired ElevenLabs audio format string.

    Returns:
        Validated format string.

    Raises:
        ValueError: If the format is not supported by ElevenLabs.
    """
    valid_formats = {
        "mp3_22050_32",
        "mp3_44100_32",
        "mp3_44100_64",
        "mp3_44100_128",
        "pcm_16000",
        "pcm_22050",
        "ulaw_8000",
        "alaw_8000",
    }
    fmt = output_format.lower()
    if fmt not in valid_formats:
        raise ValueError(
            f"Unsupported ElevenLabs audio format: {output_format}. "
            f"Choose from: {', '.join(sorted(valid_formats))}"
        )
    return fmt


def validate_voice_id(voice_id: str) -> str:
    """Validate that a voice ID looks like an ElevenLabs voice ID.

    ElevenLabs voice IDs are typically UUID-like strings.

    Args:
        voice_id: Voice identifier string.

    Returns:
        The validated voice_id.

    Raises:
        ValueError: If the voice_id format is invalid.
    """
    if not voice_id or len(voice_id) < 10:
        raise ValueError(
            f"Invalid ElevenLabs voice_id: {voice_id!r}. "
            "Expected a non-empty string of at least 10 characters."
        )
    return voice_id
