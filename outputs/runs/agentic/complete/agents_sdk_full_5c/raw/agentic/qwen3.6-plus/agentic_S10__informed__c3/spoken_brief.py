"""
Generate a spoken brief from model output text using ElevenLabs Text to Speech.

Provider: ElevenLabs TTS
SDK: elevenlabs (via requests for REST API)
Auth: ELEVENLABS_API_KEY
"""

from __future__ import annotations

import os
from typing import Optional

import requests

from model_models import SpeechResult


ELEVENLABS_API_HOST = "api.elevenlabs.io"
ELEVENLABS_TTS_API_V1 = "https://api.elevenlabs.io/v1"
DEFAULT_ELEVENLABS_VOICE_ID = "EXAVITQu4vr4xnSDxMaL"  # "Bella" voice


def load_elevenlabs_api_key() -> str:
    """Load the ElevenLabs API key from environment."""
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError(
            "ELEVENLABS_API_KEY environment variable is required. "
            "Sign up at https://elevenlabs.io/ to get your API key."
        )
    return api_key


def _build_tts_url(voice_id: str, model_id: str) -> str:
    """Construct the ElevenLabs TTS endpoint URL."""
    return f"{ELEVENLABS_TTS_API_V1}/text-to-speech/{voice_id}"


def generate_spoken_brief(
    text: str,
    voice_id: Optional[str] = None,
    model_id: str = "eleven_monolingual_v1",
    api_key: Optional[str] = None,
    output_format: str = "mp3_44100_128",
    stability: float = 0.5,
    similarity_boost: float = 0.75,
) -> SpeechResult:
    """Generate a spoken audio brief from text using ElevenLabs TTS.

    Args:
        text: The text to convert to speech.
        voice_id: ElevenLabs voice identifier. Default: 'Bella'.
        model_id: ElevenLabs model ID (e.g., 'eleven_monolingual_v1',
                  'eleven_multilingual_v2', 'eleven_turbo_v2_5').
        api_key: Optional override for the ElevenLabs API key.
        output_format: Output audio format (e.g., 'mp3_44100_128', 'pcm_16000').
        stability: Voice stability (0.0-1.0).
        similarity_boost: Voice similarity boost (0.0-1.0).

    Returns:
        SpeechResult with the generated audio data.
    """
    key = api_key or load_elevenlabs_api_key()
    target_voice = voice_id or DEFAULT_ELEVENLABS_VOICE_ID
    tts_url = _build_tts_url(target_voice, model_id)

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": key,
    }

    payload = {
        "text": text,
        "model_id": model_id,
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similarity_boost,
        },
    }

    params = {"output_format": output_format}

    response = requests.post(tts_url, headers=headers, json=payload, params=params, timeout=60)
    response.raise_for_status()

    return SpeechResult(
        audio_data=response.content,
        format="mp3" if "mp3" in output_format else "pcm",
        raw_response=response,
    )


def generate_spoken_brief_with_voice(
    text: str,
    voice_name: str,
    model_id: str = "eleven_multilingual_v2",
) -> SpeechResult:
    """Generate a spoken brief using a well-known ElevenLabs voice by name.

    Pre-mapped popular ElevenLabs voices:
        - 'Rachel': EXAVITQu4vr4xnSDxMaL
        - 'Adam': pNInz6obpgDQGcFmaJgB
        - 'Antoni': ERXwobaZiN019PkySvjV
        - 'Josh': VR6AewLTigWG4xSOukaG
        - 'Bella': MF3mGyEYCl7XYWbV9V6O
    """
    voice_map = {
        "rachel": "EXAVITQu4vr4xnSDxMaL",
        "adam": "pNInz6obpgDQGcFmaJgB",
        "antoni": "ERXwobaZiN019PkySvjV",
        "josh": "VR6AewLTigWG4xSOukaG",
        "bella": "MF3mGyEYCl7XYWbV9V6O",
    }
    resolved_voice = voice_map.get(voice_name.lower())
    if resolved_voice is None:
        resolved_voice = voice_name
    return generate_spoken_brief(text, voice_id=resolved_voice, model_id=model_id)


def generate_spoken_brief_multilingual(
    text: str,
    voice_id: Optional[str] = None,
) -> SpeechResult:
    """Generate a spoken brief using the ElevenLabs multilingual model."""
    return generate_spoken_brief(
        text=text,
        voice_id=voice_id,
        model_id="eleven_multilingual_v2",
    )
