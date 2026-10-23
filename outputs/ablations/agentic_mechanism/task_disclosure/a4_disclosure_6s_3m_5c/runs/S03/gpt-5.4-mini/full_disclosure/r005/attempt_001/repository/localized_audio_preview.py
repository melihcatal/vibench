import os
import base64
from typing import Dict, Optional

import requests


OPENAI_TTS_URL = "https://api.openai.com/v1/audio/speech"
OPENAI_TTS_MODEL = "gpt-4o-mini-tts"


def generate_spoken_preview(text: str, voice: str = "alloy", format: str = "mp3", instructions: Optional[str] = None) -> bytes:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload: Dict[str, object] = {
        "model": OPENAI_TTS_MODEL,
        "input": text,
        "voice": voice,
        "response_format": format,
    }
    if instructions:
        payload["instructions"] = instructions

    response = requests.post(
        OPENAI_TTS_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    return response.content


def generate_spoken_preview_base64(text: str, voice: str = "alloy", format: str = "mp3", instructions: Optional[str] = None) -> str:
    return base64.b64encode(generate_spoken_preview(text, voice=voice, format=format, instructions=instructions)).decode("ascii")
