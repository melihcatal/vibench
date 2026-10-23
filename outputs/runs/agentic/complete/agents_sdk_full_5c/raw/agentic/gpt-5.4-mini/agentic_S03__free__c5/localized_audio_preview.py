import os
from typing import BinaryIO

import requests


ELEVENLABS_API_KEY_ENV = "ELEVENLABS_API_KEY"
ELEVENLABS_API_HOST = "https://api.elevenlabs.io/v1/text-to-speech"
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")


def generate_audio_preview(text: str, output_format: str = "mp3") -> bytes:
    api_key = os.getenv(ELEVENLABS_API_KEY_ENV, "")
    response = requests.post(
        f"{ELEVENLABS_API_HOST}/{ELEVENLABS_VOICE_ID}",
        headers={"xi-api-key": api_key, "accept": f"audio/{output_format}"},
        json={"text": text, "model_id": "eleven_multilingual_v2"},
        timeout=60,
    )
    response.raise_for_status()
    return response.content
