from __future__ import annotations

import base64
import os

import requests


OPENAI_AUDIO_MODEL = os.getenv("OPENAI_AUDIO_MODEL", "gpt-4o-mini-tts")
OPENAI_AUDIO_VOICE = os.getenv("OPENAI_AUDIO_VOICE", "alloy")


def retrieval_audio_brief(results: list[dict[str, object]]) -> dict[str, object]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    prompt = f"Create a concise spoken brief of these retrieval results: {results}"
    response = requests.post(
        "https://api.openai.com/v1/audio/speech",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_AUDIO_MODEL,
            "voice": OPENAI_AUDIO_VOICE,
            "input": prompt,
            "format": "mp3",
        },
        timeout=60.0,
    )
    response.raise_for_status()
    audio_bytes = response.content
    return {
        "provider": "openai",
        "model": OPENAI_AUDIO_MODEL,
        "voice": OPENAI_AUDIO_VOICE,
        "audio_base64": base64.b64encode(audio_bytes).decode("ascii"),
        "mime_type": "audio/mpeg",
    }
