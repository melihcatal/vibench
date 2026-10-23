import base64
import json
import os
from typing import Any, Dict, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/audio/speech"
OPENAI_MODEL = "gpt-4o-mini-tts"


def generate_reviewer_brief_audio(brief_text: str, voice: str = "alloy", format: str = "mp3", speed: float = 1.0) -> bytes:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload: Dict[str, Any] = {
        "model": OPENAI_MODEL,
        "input": brief_text,
        "voice": voice,
        "format": format,
        "speed": speed,
    }
    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        data=json.dumps(payload),
        timeout=60,
    )
    response.raise_for_status()
    return response.content


def generate_reviewer_brief_audio_base64(brief_text: str, voice: str = "alloy", format: str = "mp3", speed: float = 1.0) -> str:
    return base64.b64encode(generate_reviewer_brief_audio(brief_text, voice=voice, format=format, speed=speed)).decode("ascii")


def main() -> None:
    import sys

    if len(sys.argv) < 2:
        raise SystemExit("usage: reviewer_brief_audio.py <brief_text>")
    audio = generate_reviewer_brief_audio(sys.argv[1])
    sys.stdout.buffer.write(audio)


if __name__ == "__main__":
    main()
