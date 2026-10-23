import os
from typing import Optional

import requests


OPENAI_TTS_API_URL = "https://api.openai.com/v1/audio/speech"
OPENAI_TTS_MODEL = "gpt-4o-mini-tts"


def synthesize_text(
    text: str,
    voice: str = "alloy",
    model: str = OPENAI_TTS_MODEL,
    api_key: Optional[str] = None,
    response_format: str = "mp3",
) -> bytes:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")
    if not text:
        raise ValueError("text must not be empty")

    payload = {
        "model": model,
        "input": text,
        "voice": voice,
        "format": response_format,
    }
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }

    response = requests.post(OPENAI_TTS_API_URL, json=payload, headers=headers, timeout=120)
    response.raise_for_status()
    return response.content
