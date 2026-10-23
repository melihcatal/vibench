from __future__ import annotations

from openai import OpenAI

from safety_client import get_openai_api_key, tts_model


def reviewer_brief_audio(brief_text: str, voice: str = "alloy", api_key: str | None = None, model: str | None = None) -> bytes:
    client = OpenAI(api_key=get_openai_api_key(api_key))
    resolved_model = tts_model(model)
    response = client.audio.speech.create(
        model=resolved_model,
        voice=voice,
        input=brief_text,
        format="mp3",
    )
    return response.read()
