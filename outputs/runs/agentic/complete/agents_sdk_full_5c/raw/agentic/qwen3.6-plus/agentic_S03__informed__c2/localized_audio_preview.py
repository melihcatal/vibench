"""Generate spoken previews of translated copy using ElevenLabs Text to Speech API.

Converts translated text segments to audio previews for review by
stakeholders using ElevenLabs' high-quality TTS voices.
"""

import os
from typing import Any

import requests


ELEVENLABS_API_URL = "https://api.elevenlabs.io/v1"
DEFAULT_VOICE_ID = "EXAVITQu4vr4xnSDxMaL"  # Rachel voice


def generate_audio_preview(
    text: str,
    language: str = "en",
    voice_id: str = DEFAULT_VOICE_ID,
    model_id: str = "eleven_multilingual_v2",
    output_format: str = "mp3_44100_128",
) -> dict[str, Any]:
    """Generate a spoken audio preview of translated text using ElevenLabs TTS.

    Args:
        text: The translated text to convert to speech.
        language: Target language code for the preview (e.g., 'en', 'es', 'fr', 'de', 'ja').
        voice_id: ElevenLabs voice identifier.
        model_id: ElevenLabs model identifier (eleven_multilingual_v2 supports many languages).
        output_format: Audio output format string.

    Returns:
        Dictionary containing audio bytes, metadata, and the voice/model used.
    """
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable is required for ElevenLabs TTS API")

    url = f"{ELEVENLABS_API_URL}/text-to-speech/{voice_id}"

    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
    }

    payload: dict[str, Any] = {
        "text": text,
        "model_id": model_id,
        "output_format": output_format,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
        },
    }

    response = requests.post(url, headers=headers, json=payload, timeout=60)
    response.raise_for_status()

    audio_bytes = response.content

    return {
        "audio": audio_bytes,
        "text": text,
        "language": language,
        "voice_id": voice_id,
        "model_id": model_id,
        "output_format": output_format,
        "provider": "elevenlabs",
        "audio_size_bytes": len(audio_bytes),
    }


def generate_batch_audio_previews(
    texts: list[str],
    language: str = "en",
    voice_id: str = DEFAULT_VOICE_ID,
    model_id: str = "eleven_multilingual_v2",
    output_format: str = "mp3_44100_128",
) -> list[dict[str, Any]]:
    """Generate spoken audio previews for multiple translated texts using ElevenLabs TTS.

    Args:
        texts: List of translated text strings to convert to speech.
        language: Target language code for the previews.
        voice_id: ElevenLabs voice identifier.
        model_id: ElevenLabs model identifier.
        output_format: Audio output format string.

    Returns:
        List of audio preview result dictionaries corresponding to each input text.
    """
    results: list[dict[str, Any]] = []
    for text in texts:
        result = generate_audio_preview(
            text=text,
            language=language,
            voice_id=voice_id,
            model_id=model_id,
            output_format=output_format,
        )
        results.append(result)
    return results


def list_available_voices() -> list[dict[str, Any]]:
    """List available ElevenLabs TTS voices.

    Returns:
        List of voice metadata dictionaries with name, language, and voice_id.
    """
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable is required for ElevenLabs TTS API")

    url = f"{ELEVENLABS_API_URL}/voices"
    headers = {"xi-api-key": api_key}

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    data = response.json()

    voices = data.get("voices", [])
    return [
        {
            "voice_id": v.get("voice_id"),
            "name": v.get("name"),
            "labels": v.get("labels", {}),
            "category": v.get("category"),
        }
        for v in voices
    ]
