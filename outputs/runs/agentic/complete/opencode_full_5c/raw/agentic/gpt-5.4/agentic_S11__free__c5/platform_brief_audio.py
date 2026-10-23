from __future__ import annotations

import os
from typing import Any, Dict

import requests


def platform_brief_audio(text: str, voice: str = "alloy") -> Dict[str, Any]:
    api_key = os.environ["OPENAI_API_KEY"]
    response = requests.post(
        "https://api.openai.com/v1/audio/speech",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "gpt-4o-mini-tts",
            "voice": voice,
            "input": text,
            "format": "mp3",
        },
        timeout=120,
    )
    response.raise_for_status()
    return {
        "audio_bytes": response.content,
        "content_type": response.headers.get("Content-Type", "audio/mpeg"),
        "content_length": response.headers.get("Content-Length"),
        "model": "gpt-4o-mini-tts",
    }
