import os
from typing import Any, Dict, Optional

import requests


OPENAI_TTS_API_URL = "https://api.openai.com/v1/audio/speech"
OPENAI_TTS_MODEL = os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")
OPENAI_TTS_VOICE = os.getenv("OPENAI_TTS_VOICE", "alloy")


def generate_localized_audio_preview(
    text: str,
    language: str,
    output_path: str,
    instructions: Optional[str] = None,
    timeout: int = 60,
) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload: Dict[str, Any] = {
        "model": OPENAI_TTS_MODEL,
        "voice": OPENAI_TTS_VOICE,
        "input": text,
        "response_format": "mp3",
    }
    if instructions:
        payload["instructions"] = instructions
    else:
        payload["instructions"] = f"Speak clearly in {language} for a localized audio preview."

    response = requests.post(OPENAI_TTS_API_URL, headers=headers, json=payload, timeout=timeout)
    response.raise_for_status()

    with open(output_path, "wb") as f:
        f.write(response.content)

    return output_path
