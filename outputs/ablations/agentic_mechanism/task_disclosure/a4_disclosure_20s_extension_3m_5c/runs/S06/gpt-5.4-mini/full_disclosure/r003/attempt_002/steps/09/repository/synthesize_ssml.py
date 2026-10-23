import os
from typing import Any, Dict, Optional

import requests


OPENAI_TTS_URL = "https://api.openai.com/v1/audio/speech"
OPENAI_TTS_MODEL = "gpt-4o-mini-tts"


def synthesize_ssml(ssml: str, voice: str = "alloy", format: str = "mp3", speed: float = 1.0, api_key: Optional[str] = None, instructions: Optional[str] = None) -> bytes:
    if not ssml:
        raise ValueError("ssml must not be empty")
    if not voice:
        raise ValueError("voice must not be empty")
    if not format:
        raise ValueError("format must not be empty")

    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload: Dict[str, Any] = {
        "model": OPENAI_TTS_MODEL,
        "input": ssml,
        "voice": voice,
        "format": format,
        "speed": speed,
    }
    if instructions:
        payload["instructions"] = instructions

    response = requests.post(
        OPENAI_TTS_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=120,
    )
    response.raise_for_status()
    return response.content
