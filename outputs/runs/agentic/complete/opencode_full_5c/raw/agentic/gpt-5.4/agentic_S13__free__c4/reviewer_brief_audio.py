from __future__ import annotations

from openai import OpenAI


AUDIO_MODEL = "gpt-4o-mini-tts"


def reviewer_brief_audio(brief_text: str, voice: str = "alloy") -> bytes:
    client = OpenAI()
    response = client.audio.speech.create(
        model=AUDIO_MODEL,
        voice=voice,
        input=brief_text,
        format="mp3",
    )
    return response.read()
