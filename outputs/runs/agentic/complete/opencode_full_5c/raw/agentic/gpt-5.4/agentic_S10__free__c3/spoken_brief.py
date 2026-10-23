from __future__ import annotations

import base64

from model_client import DEFAULT_AUDIO_MODEL, get_openai_client


def generate_spoken_brief(
    text: str, voice: str = "alloy", audio_format: str = "mp3"
) -> dict:
    client = get_openai_client()
    response = client.audio.speech.create(
        model=DEFAULT_AUDIO_MODEL,
        voice=voice,
        input=text,
        format=audio_format,
    )
    audio_bytes = response.read()
    return {
        "audio_base64": base64.b64encode(audio_bytes).decode("ascii"),
        "model": DEFAULT_AUDIO_MODEL,
        "voice": voice,
        "format": audio_format,
    }
