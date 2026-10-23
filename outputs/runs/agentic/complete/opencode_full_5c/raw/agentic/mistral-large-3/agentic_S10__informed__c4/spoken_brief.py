import os
from typing import Dict, Any
import requests


def spoken_brief(
    text: str, voice_id: str = "EXAVITQu4vr4xnSDxMaL", api_key: str = None
) -> bytes:
    """
    Generates a spoken brief from the model output using ElevenLabs Text-to-Speech.

    Args:
        text: Text to convert to speech.
        voice_id: ElevenLabs voice ID.
        api_key: ElevenLabs API key. Defaults to ELEVENLABS_API_KEY environment variable.

    Returns:
        Audio data as bytes.
    """
    api_key = api_key or os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set")

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key,
    }

    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.5},
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()

    return response.content
