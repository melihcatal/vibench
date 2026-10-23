import os
import requests
import json


def generate_spoken_brief(text: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM") -> bytes:
    """
    Generate a spoken brief from model output using ElevenLabs Text-to-Speech.
    """
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable must be set")

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {"xi-api-key": api_key, "Content-Type": "application/json"}

    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

    return response.content


def get_available_voices() -> list:
    """
    Get available voices from ElevenLabs.
    """
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable must be set")

    url = "https://api.elevenlabs.io/v1/voices"

    headers = {"xi-api-key": api_key}

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    voices_data = response.json()
    return voices_data.get("voices", [])
