import os
from typing import Optional

import requests


OPENAI_TTS_ENDPOINT = "https://api.openai.com/v1/audio/speech"


def _ssml_to_openai_input(ssml: str) -> str:
    return ssml


def synthesize_ssml_to_audio_bytes(
    ssml: str,
    *,
    model: str = "gpt-4o-mini-tts",
    voice: str = "alloy",
    response_format: str = "mp3",
    speed: Optional[float] = None,
    api_key: Optional[str] = None,
) -> bytes:
    payload = {
        "model": model,
        "input": _ssml_to_openai_input(ssml),
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
    return response.content


def synthesize_ssml(ssml: str, **kwargs) -> bytes:
    return synthesize_ssml_to_audio_bytes(ssml, **kwargs)
