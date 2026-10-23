from __future__ import annotations

import os

from openai import OpenAI

from model_models import SpeechRequest

TTS_MODEL = "gpt-4o-mini-tts"


def spoken_brief(text: str, voice: str = "alloy", model: str | None = None) -> bytes:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    req = SpeechRequest(text=text, voice=voice, model=model or TTS_MODEL)
    response = client.audio.speech.create(
        model=req.model,
        voice=req.voice,
        input=req.text,
        format="mp3",
    )
    return response.read()
