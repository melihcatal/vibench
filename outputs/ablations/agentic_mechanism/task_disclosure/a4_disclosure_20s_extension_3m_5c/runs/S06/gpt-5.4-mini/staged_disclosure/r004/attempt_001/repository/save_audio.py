import base64
import os
from pathlib import Path
from typing import Optional, Union

import requests


OPENAI_TTS_URL = "https://api.openai.com/v1/audio/speech"
OPENAI_TTS_MODEL = "gpt-4o-mini-tts"


def synthesize_speech(
    text: str,
    output: Optional[Union[str, Path]] = None,
    *,
    voice: str = "alloy",
    format: str = "mp3",
    as_bytes: bool = False,
) -> Union[bytes, str]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")

    response = requests.post(
        OPENAI_TTS_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_TTS_MODEL,
            "input": text,
            "voice": voice,
            "format": format,
        },
        timeout=60,
    )
    response.raise_for_status()

    audio_bytes = response.content
    if output is not None:
        path = Path(output)
        path.write_bytes(audio_bytes)
        return str(path)

    if as_bytes:
        return audio_bytes

    return base64.b64encode(audio_bytes).decode("ascii")
