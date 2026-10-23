from __future__ import annotations

from typing import Dict

from model_client import OPENAI_DEFAULT_TTS_MODEL, get_openai_client


def platform_brief_audio(text: str, voice: str = "alloy") -> Dict[str, object]:
    client = get_openai_client()
    response = client.audio.speech.create(
        model=OPENAI_DEFAULT_TTS_MODEL,
        voice=voice,
        input=text,
        format="mp3",
    )
    audio_bytes = response.read()
    return {
        "provider": "openai",
        "model": OPENAI_DEFAULT_TTS_MODEL,
        "voice": voice,
        "audio_bytes": audio_bytes,
        "content_type": "audio/mpeg",
    }
