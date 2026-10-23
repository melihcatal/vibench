import base64
import json
import os
from typing import Optional

import requests


OPENAI_TTS_ENDPOINT = "https://api.openai.com/v1/audio/speech"


def synthesize_text_to_audio_bytes(
    text: str,
    *,
    model: str = "gpt-4o-mini-tts",
    voice: str = "alloy",
    response_format: str = "mp3",
    speed: Optional[float] = None,
    api_key: Optional[str] = None,
) -> bytes:
    payload = {
        "model": model,
        "input": text,
        "voice": voice,
        "response_format": response_format,
    }
    if speed is not None:
        payload["speed"] = speed
    headers = {
        "Authorization": f"Bearer {api_key or os.environ.get('OPENAI_API_KEY', '')}",
        "Content-Type": "application/json",
    }
    response = requests.post(OPENAI_TTS_ENDPOINT, headers=headers, json=payload, timeout=120)
    response.raise_for_status()
    content_type = response.headers.get("Content-Type", "")
    if "application/json" in content_type:
        data = response.json()
        if "audio" in data:
            return base64.b64decode(data["audio"])
        if "data" in data:
            return base64.b64decode(data["data"])
        raise ValueError("Unexpected JSON response from OpenAI TTS API")
    return response.content


def synthesize_text(text: str, **kwargs) -> bytes:
    return synthesize_text_to_audio_bytes(text, **kwargs)
