import os
import requests
from typing import List

# Example: using ElevenLabs Text-to-Speech SDK
# Requires ELEVENLABS_API_KEY environment variable

API_KEY = os.getenv("ELEVENLABS_API_KEY")
if not API_KEY:
    raise ValueError("ELEVENLABS_API_KEY environment variable not set")

BASE_URL = "https://api.elevenlabs.io/v1/text-to-speech"


def generate_audio_brief(summary_text: str, voice_id: str = "1"):
    """Generate a spoken audio brief from retrieved search results using ElevenLabs TTS.

    Returns the audio data as binary bytes.
    """
    payload = {
        "text": summary_text,
        "voice_id": voice_id,
        "model_id": "eleven_monolingual_v1",
    }
    headers = {"xi-api-key": API_KEY, "Content-Type": "application/json"}
    response = requests.post(BASE_URL, json=payload, headers=headers)
    response.raise_for_status()
    # Return raw audio bytes (MP3 format by default)
    return response.content
