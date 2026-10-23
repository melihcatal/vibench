from __future__ import annotations

from safety_client import OPENAI_TTS_MODEL, get_openai_client


def generate_reviewer_brief_audio(brief_text: str, voice: str = "alloy") -> bytes:
    client = get_openai_client()
    response = client.audio.speech.create(
        model=OPENAI_TTS_MODEL,
        voice=voice,
        input=brief_text,
        format="mp3",
    )
    return response.read()
