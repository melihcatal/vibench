import os
from typing import Any, Dict, Optional

import requests


OPENAI_TTS_ENDPOINT = "https://api.openai.com/v1/audio/speech"
OPENAI_TTS_MODEL = "gpt-4o-mini-tts"


def build_briefing_text(platform_output: Any) -> str:
    if isinstance(platform_output, str):
        text = platform_output.strip()
    else:
        text = str(platform_output).strip()
    return text or "No platform output was provided."


def generate_spoken_briefing(platform_output: Any, output_path: str, voice: str = "alloy", speed: float = 1.0, api_key: Optional[str] = None) -> str:
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")

    payload: Dict[str, Any] = {
        "model": OPENAI_TTS_MODEL,
        "input": build_briefing_text(platform_output),
        "voice": voice,
        "speed": speed,
        "response_format": "mp3",
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    response = requests.post(OPENAI_TTS_ENDPOINT, json=payload, headers=headers, timeout=60)
    response.raise_for_status()

    with open(output_path, "wb") as audio_file:
        audio_file.write(response.content)

    return output_path
