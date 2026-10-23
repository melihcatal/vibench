from __future__ import annotations

import os

from openai import OpenAI


AUDIO_MODEL = "gpt-4o-mini-tts"
AUDIO_VOICE = "alloy"


def reviewer_brief_audio(brief_text: str) -> bytes:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.audio.speech.create(
        model=AUDIO_MODEL,
        voice=AUDIO_VOICE,
        input=brief_text,
        format="mp3",
    )
    return response.read()
