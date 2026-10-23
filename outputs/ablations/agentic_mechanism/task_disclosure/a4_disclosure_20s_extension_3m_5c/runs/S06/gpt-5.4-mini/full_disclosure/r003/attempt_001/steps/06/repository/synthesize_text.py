import os
from typing import Optional

import requests


OPENAI_TTS_URL = "https://api.openai.com/v1/audio/speech"
OPENAI_TTS_MODEL = "gpt-4o-mini-tts"


def synthesize_text(text: str, voice: str = "alloy", model: str = OPENAI_TTS_MODEL, format: str = "mp3", speed: Optional[float] = None) -> bytes:
    payload = {"model": model, "input": text, "voice": voice, "format": format}
    if speed is not None:
        payload["speed"] = speed

    response = requests.post(
        OPENAI_TTS_URL,
        headers={
            "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=120,
    )
    response.raise_for_status()
    return response.content
