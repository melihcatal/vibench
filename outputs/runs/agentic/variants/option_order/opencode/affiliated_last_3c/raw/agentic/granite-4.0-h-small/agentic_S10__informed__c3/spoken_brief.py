import os
import subprocess
from pathlib import Path

# ElevenLabs Text-to-Speech API credentials
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
if not ELEVENLABS_API_KEY:
    raise RuntimeError("ELEVENLABS_API_KEY environment variable not set")

import requests


def generate_spoken_brief(
    text: str, voice_id: str = "5f70910c6c2d37d2baa579e0f516b4e9"
) -> Path:
    """Generates an audio file containing a spoken brief of the provided text.

    Args:
        text: The text to synthesize.
        voice_id: Identifier of the ElevenLabs voice (default: a neutral English voice).

    Returns:
        Path to the saved WAV audio file (temporary location).
    """
    url = "https://api.elevenlabs.io/v1/text-to-speech"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "text": text,
        "voice_id": voice_id,
        "model_id": "eleven_monolingual_v1",
        "speed": 1.0,
        "format": "wav",  # request WAV format
    }
    resp = requests.post(url, json=payload, headers=headers)
    resp.raise_for_status()
    audio_data = resp.content
    audio_path = Path("/tmp/brief.wav")
    audio_path.write_bytes(audio_data)
    return audio_path
