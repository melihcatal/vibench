from __future__ import annotations

import os
from typing import Optional

from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
TTS_MODEL = os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")
VOICE = os.getenv("OPENAI_TTS_VOICE", "alloy")


def platform_brief_audio(text: str, output_file: Optional[str] = None) -> bytes:
    client = OpenAI(api_key=OPENAI_API_KEY or None)
    response = client.audio.speech.create(model=TTS_MODEL, voice=VOICE, input=text)
    audio_bytes = response.read()
    if output_file:
        with open(output_file, "wb") as f:
            f.write(audio_bytes)
    return audio_bytes
