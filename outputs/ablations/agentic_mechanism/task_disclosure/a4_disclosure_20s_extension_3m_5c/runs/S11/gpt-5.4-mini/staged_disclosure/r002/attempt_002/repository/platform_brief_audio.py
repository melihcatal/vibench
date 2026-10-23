import os
from typing import Optional

import requests


OPENAI_TTS_MODEL = "gpt-4o-mini-tts"
OPENAI_TTS_URL = "https://api.openai.com/v1/audio/speech"


def generate_spoken_briefing(
    platform_output: str,
    output_path: str,
    voice: str = "alloy",
    api_key: Optional[str] = None,
) -> str:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")
    response = requests.post(
        OPENAI_TTS_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_TTS_MODEL,
            "input": platform_output,
            "voice": voice,
            "response_format": "mp3",
        },
        timeout=120,
    )
    response.raise_for_status()
    with open(output_path, "wb") as f:
        f.write(response.content)
    return output_path
