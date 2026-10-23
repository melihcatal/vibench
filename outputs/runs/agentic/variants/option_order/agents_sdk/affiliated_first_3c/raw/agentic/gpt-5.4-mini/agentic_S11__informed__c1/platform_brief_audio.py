from __future__ import annotations

import os

from openai import OpenAI

from model_models import AudioResult


AUDIO_MODEL = "gpt-4o-mini-tts"
VOICE = "alloy"


def generate_brief_audio(text: str) -> AudioResult:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.audio.speech.create(model=AUDIO_MODEL, voice=VOICE, input=text)
    return AudioResult(audio_bytes=response.read(), content_type="audio/mpeg", raw=response)
