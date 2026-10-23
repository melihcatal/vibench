from __future__ import annotations

import os
from typing import Optional

import requests


OPENAI_TTS_URL = "https://api.openai.com/v1/audio/speech"
DEFAULT_MODEL = "gpt-4o-mini-tts"
DEFAULT_VOICE = "alloy"


def synthesize_text(text: str, voice: str = DEFAULT_VOICE, model: str = DEFAULT_MODEL, response_format: str = "mp3", api_key: Optional[str] = None) -> bytes:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")
    response = requests.post(
        OPENAI_TTS_URL,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json={"model": model, "input": text, "voice": voice, "response_format": response_format},
        timeout=120,
    )
    response.raise_for_status()
    return response.content
