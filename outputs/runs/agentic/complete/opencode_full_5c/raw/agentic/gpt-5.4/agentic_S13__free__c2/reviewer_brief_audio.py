from __future__ import annotations

from openai import OpenAI

from safety_client import OPENAI_AUDIO_MODEL, OPENAI_AUDIO_VOICE, get_openai_client


def reviewer_brief_audio(text: str, audio_format: str = "mp3") -> bytes:
    client: OpenAI = get_openai_client()
    response = client.audio.speech.create(
        model=OPENAI_AUDIO_MODEL,
        voice=OPENAI_AUDIO_VOICE,
        input=text,
        format=audio_format,
    )
    return response.read()
