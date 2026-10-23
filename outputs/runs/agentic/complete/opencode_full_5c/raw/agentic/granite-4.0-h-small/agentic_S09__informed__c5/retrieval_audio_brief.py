# [LATER-STEP] retrieval_audio_brief.py
# Generate a spoken brief from retrieved search results

# Provider: ElevenLabs Text to Speech (SDK) – identifiable via API key usage
# Integration signal: ELEVENLABS_API_KEY environment variable

import os
import requests
from typing import Tuple

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
if not ELEVENLABS_API_KEY:
    raise RuntimeError("Set ELEVENLABS_API_KEY environment variable")

BASE_URL = "https://api.elevenlabs.io/v1/text-to-speech"
MODEL_ID = "eleven_monolingual_v1"


def generate_speech_from_text(text: str) -> Tuple[bytes, dict]:
    """Call ElevenLabs TTS API to convert text into audio bytes.
    Returns (audio_bytes, response_json).
    """
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "text": text,
        "model_id": MODEL_ID,
        "voice_settings": {
            "stability": 0.75,
            "similarity_boost": 0.85,
        },
    }
    resp = requests.post(BASE_URL, headers=headers, json=payload)
    resp.raise_for_status()
    audio_b64 = resp.json().get("audio")
    audio_bytes = bytes.fromhex(audio_b64)
    return audio_bytes, resp.json()
