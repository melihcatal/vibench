import os
from typing import Optional

import requests


def generate_audio_preview(
    text: str,
    voice_id: Optional[str] = None,
    model_id: str = "eleven_multilingual_v2",
    output_format: str = "mp3_44100_128",
    stability: float = 0.5,
    similarity_boost: float = 0.75,
) -> bytes:
    api_key = os.environ.get("ELEVENLABS_API_KEY", "")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable is required")

    voice = voice_id or "EXAVITQu4vr4xnSDxMaL"

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice}"

    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
    }

    body = {
        "text": text,
        "model_id": model_id,
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similarity_boost,
        },
        "output_format": output_format,
    }

    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()

    return response.content


def generate_audio_preview_for_segments(
    segments: list[str],
    voice_id: Optional[str] = None,
    model_id: str = "eleven_multilingual_v2",
    output_format: str = "mp3_44100_128",
) -> list[bytes]:
    audio_previews = []
    for segment in segments:
        audio_data = generate_audio_preview(
            text=segment,
            voice_id=voice_id,
            model_id=model_id,
            output_format=output_format,
        )
        audio_previews.append(audio_data)
    return audio_previews
