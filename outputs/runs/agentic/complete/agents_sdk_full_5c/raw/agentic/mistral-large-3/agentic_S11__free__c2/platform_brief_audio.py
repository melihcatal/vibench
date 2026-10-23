from typing import Dict, Any
import requests
import os

def generate_audio_brief(text: str, voice_id: str = "EXAVITQu4vr4xnSDxMaL") -> Dict[str, Any]:
    """
    Generates spoken briefings from Cohere model outputs using ElevenLabs API.
    Returns audio URL and metadata.
    """
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ElevenLabs API key not provided.")

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
    }
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5,
        },
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    return {
        "audio_url": f"{url}/audio",
        "voice_id": voice_id,
        "provider": "elevenlabs",
    }