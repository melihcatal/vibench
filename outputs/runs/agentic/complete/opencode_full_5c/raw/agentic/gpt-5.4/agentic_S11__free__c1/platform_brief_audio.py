from __future__ import annotations

from model_client import get_openai_client, get_tts_model, get_tts_voice


def platform_brief_audio(text: str) -> bytes:
    client = get_openai_client()
    audio = client.audio.speech.create(
        model=get_tts_model(),
        voice=get_tts_voice(),
        input=text,
        format="mp3",
    )
    return audio.read()
