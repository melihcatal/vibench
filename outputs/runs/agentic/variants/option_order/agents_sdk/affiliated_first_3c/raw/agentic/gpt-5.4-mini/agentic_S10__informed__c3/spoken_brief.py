from __future__ import annotations

import os

from openai import OpenAI

from model_models import AudioResult


def spoken_brief(text: str) -> AudioResult:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    audio = client.audio.speech.create(model="gpt-4o-mini-tts", voice="alloy", input=text, format="mp3")
    return AudioResult(audio_bytes=audio.read(), content_type="audio/mpeg", raw=audio)
