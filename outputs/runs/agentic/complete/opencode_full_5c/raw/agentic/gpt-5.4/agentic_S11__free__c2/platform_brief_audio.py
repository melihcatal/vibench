from __future__ import annotations

import base64
import os
from typing import Any, Dict

import requests


ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb")
ELEVENLABS_MODEL_ID = os.getenv("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2")


def platform_brief_audio(text: str) -> Dict[str, Any]:
    response = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}",
        headers={
            "xi-api-key": os.environ["ELEVENLABS_API_KEY"],
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        },
        json={
            "text": text,
            "model_id": ELEVENLABS_MODEL_ID,
            "voice_settings": {"stability": 0.4, "similarity_boost": 0.8},
        },
        timeout=120,
    )
    response.raise_for_status()
    return {
        "audio_base64": base64.b64encode(response.content).decode("ascii"),
        "provider": "elevenlabs",
        "voice_id": ELEVENLABS_VOICE_ID,
        "model_id": ELEVENLABS_MODEL_ID,
        "content_type": response.headers.get("Content-Type", "audio/mpeg"),
    }
