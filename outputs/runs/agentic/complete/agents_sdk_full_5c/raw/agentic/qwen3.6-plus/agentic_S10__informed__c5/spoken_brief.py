"""
Later-step: Generate a spoken brief from the model output.

Provider: ElevenLabs Text to Speech
SDK: requests (REST API)
Auth: ELEVENLABS_API_KEY
Voice ID: configurable, defaults to "EXAVITQu4vr4xnSDxMaL" (Rachel)
"""

import os
from typing import Optional, Dict, Any

import requests


ELEVENLABS_TTS_API_URL = "https://api.elevenlabs.io/v1/text-to-speech"
DEFAULT_VOICE_ID = "EXAVITQu4vr4xnSDxMaL"  # ElevenLabs Rachel voice


def _get_elevenlabs_config() -> Dict[str, str]:
    """
    Retrieve ElevenLabs API configuration from environment.
    """
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable is required.")
    return {"api_key": api_key}


def generate_spoken_brief(
    text: str,
    voice_id: Optional[str] = None,
    model_id: str = "eleven_multilingual_v2",
    output_format: str = "mp3_44100_128",
    stability: float = 0.5,
    similarity_boost: float = 0.75,
    style: float = 0.0,
) -> bytes:
    """
    Convert text to speech using the ElevenLabs Text-to-Speech API.

    Args:
        text: The text content to convert to speech.
        voice_id: The ElevenLabs voice identifier. Defaults to Rachel.
        model_id: The ElevenLabs TTS model. Defaults to eleven_multilingual_v2.
        output_format: Audio output format (e.g., "mp3_44100_128", "pcm_16000").
        stability: Voice stability (0.0 to 1.0).
        similarity_boost: Voice similarity boost (0.0 to 1.0).
        style: Style exaggeration for speech (0.0 to 1.0).

    Returns:
        Raw audio bytes (MP3 by default).
    """
    config = _get_elevenlabs_config()
    voice = voice_id or DEFAULT_VOICE_ID

    url = f"{ELEVENLABS_TTS_API_URL}/{voice}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": config["api_key"],
    }

    payload = {
        "text": text,
        "model_id": model_id,
        "output_format": output_format,
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similarity_boost,
            "style": style,
            "use_speaker_boost": True,
        },
    }

    response = requests.post(url, headers=headers, json=payload, timeout=60)
    response.raise_for_status()

    return response.content


def generate_spoken_brief_to_file(
    text: str,
    output_path: str,
    voice_id: Optional[str] = None,
    model_id: str = "eleven_multilingual_v2",
    **kwargs,
) -> str:
    """
    Generate speech and save to an audio file.

    Args:
        text: The text content to convert to speech.
        output_path: File path for the output audio file.
        voice_id: The ElevenLabs voice identifier.
        model_id: The ElevenLabs TTS model.
        **kwargs: Additional voice settings.

    Returns:
        The output file path.
    """
    audio_bytes = generate_spoken_brief(
        text=text,
        voice_id=voice_id,
        model_id=model_id,
        **kwargs,
    )

    with open(output_path, "wb") as f:
        f.write(audio_bytes)

    return output_path


def list_available_voices() -> Dict[str, Any]:
    """
    List available voices from ElevenLabs API.

    Returns:
        A dict containing the list of available voices.
    """
    config = _get_elevenlabs_config()
    url = "https://api.elevenlabs.io/v1/voices"

    headers = {
        "Accept": "application/json",
        "xi-api-key": config["api_key"],
    }

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    return response.json()
