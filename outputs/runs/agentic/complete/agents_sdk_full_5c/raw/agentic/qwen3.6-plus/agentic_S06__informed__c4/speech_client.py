"""
Local helper utilities for ElevenLabs Text-to-Speech client configuration.

Provider: ElevenLabs Text to Speech
SDK: elevenlabs
Auth: ELEVENLABS_API_KEY
"""

import os
from typing import Optional

from elevenlabs import ElevenLabs

ELEVENLABS_API_KEY_ENV = "ELEVENLABS_API_KEY"

# Default model identifiers for ElevenLabs
DEFAULT_TTS_MODEL = "eleven_multilingual_v2"
DEFAULT_TTS_MODEL_V1 = "eleven_monolingual_v1"


def get_elevenlabs_client(
    api_key: Optional[str] = None,
) -> ElevenLabs:
    """Create an authenticated ElevenLabs TTS client.

    Args:
        api_key: ElevenLabs API key. Falls back to ELEVENLABS_API_KEY env var.

    Returns:
        An initialized ElevenLabs client instance.
    """
    key = api_key or os.environ.get(ELEVENLABS_API_KEY_ENV)
    if not key:
        raise ValueError(
            f"ElevenLabs API key not provided. Set {ELEVENLABS_API_KEY_ENV}."
        )
    return ElevenLabs(api_key=key)


def get_voice_config(
    voice_id: Optional[str] = None,
    model_id: Optional[str] = None,
    stability: float = 0.5,
    similarity: float = 0.75,
) -> dict:
    """Build a voice configuration dict for ElevenLabs generation.

    Args:
        voice_id: ElevenLabs voice identifier (e.g. 'EXAVITQu4vr4xnSDxMaL').
        model_id: ElevenLabs model id (e.g. 'eleven_multilingual_v2').
        stability: Voice stability (0.0 to 1.0).
        similarity: Voice similarity boost (0.0 to 1.0).

    Returns:
        Configuration dict for ElevenLabs generate calls.
    """
    return {
        "voice_id": voice_id or "EXAVITQu4vr4xnSDxMaL",  # Default Rachel voice
        "model": model_id or DEFAULT_TTS_MODEL,
        "output_format": "mp3_44100_128",
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similarity,
        },
    }


def normalize_voice_settings(
    stability: float,
    similarity_boost: float,
    style: float = 0.0,
    use_speaker_boost: bool = True,
) -> dict:
    """Normalize and clamp voice settings for ElevenLabs.

    Args:
        stability: Clamped to [0.0, 1.0].
        similarity_boost: Clamped to [0.0, 1.0].
        style: Style exaggeration, clamped to [0.0, 1.0].
        use_speaker_boost: Whether to use speaker boost.

    Returns:
        Normalized voice_settings dict.
    """
    return {
        "stability": max(0.0, min(1.0, stability)),
        "similarity_boost": max(0.0, min(1.0, similarity_boost)),
        "style": max(0.0, min(1.0, style)),
        "use_speaker_boost": use_speaker_boost,
    }
