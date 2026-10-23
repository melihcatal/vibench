from __future__ import annotations

import base64

from model_client import get_openai_client, select_model


def generate_spoken_brief(
    text: str, voice: str = "alloy", model: str | None = None, audio_format: str = "mp3"
) -> dict:
    client = get_openai_client()
    speech_model = select_model("speech", model)
    response = client.audio.speech.create(
        model=speech_model,
        voice=voice,
        input=text,
        format=audio_format,
    )
    audio_bytes = response.read()
    return {
        "model": speech_model,
        "voice": voice,
        "format": audio_format,
        "audio_base64": base64.b64encode(audio_bytes).decode("ascii"),
    }
