from __future__ import annotations

import base64

from openai import OpenAI

from safety_client import openai_config


def reviewer_brief_audio(brief_text: str, voice: str = "alloy") -> bytes:
    config = openai_config()
    client = OpenAI(api_key=config["api_key"])
    response = client.audio.speech.create(
        model=config["tts_model"],
        voice=voice,
        input=brief_text,
        format="mp3",
    )
    audio_b64 = getattr(response, "audio", None)
    if isinstance(audio_b64, str):
        return base64.b64decode(audio_b64)
    return response.read()
