import base64
import json
import os
from typing import Any, Dict, Optional

import requests


OPENAI_TTS_URL = "https://api.openai.com/v1/audio/speech"
OPENAI_TTS_MODEL = "gpt-4o-mini-tts"


def synthesize_text(text: str, voice: str = "alloy", format: str = "mp3", speed: float = 1.0, api_key: Optional[str] = None) -> bytes:
    if not text:
        raise ValueError("text must not be empty")
    if not voice:
        raise ValueError("voice must not be empty")
    if not format:
        raise ValueError("format must not be empty")

    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload: Dict[str, Any] = {
        "model": OPENAI_TTS_MODEL,
        "input": text,
        "voice": voice,
        "format": format,
        "speed": speed,
    }

    response = requests.post(
        OPENAI_TTS_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        data=json.dumps(payload),
        timeout=120,
    )
    response.raise_for_status()
    return response.content


def synthesize_text_base64(text: str, voice: str = "alloy", format: str = "mp3", speed: float = 1.0, api_key: Optional[str] = None) -> str:
    return base64.b64encode(synthesize_text(text, voice=voice, format=format, speed=speed, api_key=api_key)).decode("ascii")
