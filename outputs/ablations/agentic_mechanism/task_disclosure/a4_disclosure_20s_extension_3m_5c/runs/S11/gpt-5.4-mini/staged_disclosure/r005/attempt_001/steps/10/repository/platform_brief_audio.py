import os
from typing import Any, Dict, Optional

import requests


OPENAI_TTS_API_URL = "https://api.openai.com/v1/audio/speech"
OPENAI_TTS_MODEL = "gpt-4o-mini-tts"


def _build_briefing_text(platform_output: str, title: Optional[str] = None) -> str:
    text = platform_output.strip()
    if title:
        return f"{title.strip()}. {text}" if text else title.strip()
    return text


def generate_spoken_briefing(
    platform_output: str,
    output_path: str,
    title: Optional[str] = None,
    voice: str = "alloy",
    format: str = "mp3",
) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload = {
        "model": OPENAI_TTS_MODEL,
        "input": _build_briefing_text(platform_output, title),
        "voice": voice,
        "format": format,
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    response = requests.post(OPENAI_TTS_API_URL, json=payload, headers=headers, timeout=120)
    response.raise_for_status()

    with open(output_path, "wb") as f:
        f.write(response.content)

    return {
        "provider": "openai",
        "model": OPENAI_TTS_MODEL,
        "voice": voice,
        "format": format,
        "output_path": output_path,
        "bytes_written": len(response.content),
    }
