from __future__ import annotations

import os

from elevenlabs import ElevenLabs

from model_models import SpokenBriefRequest


def generate_spoken_brief(request: SpokenBriefRequest) -> bytes:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY is required")
    client = ElevenLabs(api_key=api_key)
    audio = client.text_to_speech.convert(
        voice_id=request.voice_id,
        model_id=request.model_id,
        output_format=request.output_format,
        text=request.text,
    )
    return b"".join(audio)
