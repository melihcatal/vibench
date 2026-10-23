import os
from typing import Dict

import requests

ELEVENLABS_API_URL = "https://api.elevenlabs.io/v1/text-to-speech"
ELEVENLABS_API_KEY_ENV = "ELEVENLABS_API_KEY"
ELEVENLABS_MODEL = "eleven_multilingual_v2"


def generate_spoken_preview(text: str, voice_id: str) -> Dict[str, str]:
    api_key = os.getenv(ELEVENLABS_API_KEY_ENV, "")
    if not api_key:
        raise ValueError(f"Missing {ELEVENLABS_API_KEY_ENV}")
    resp = requests.post(
        f"{ELEVENLABS_API_URL}/{voice_id}",
        headers={"xi-api-key": api_key, "Content-Type": "application/json"},
        json={"text": text, "model_id": ELEVENLABS_MODEL},
        timeout=30,
    )
    resp.raise_for_status()
    return {"audio_content_type": resp.headers.get("content-type", "audio/mpeg"), "preview_bytes": str(len(resp.content))}
