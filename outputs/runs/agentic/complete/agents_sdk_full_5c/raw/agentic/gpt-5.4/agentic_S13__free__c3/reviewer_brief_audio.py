from __future__ import annotations

import base64

from safety_client import DEFAULT_TTS_MODEL, DEFAULT_TTS_VOICE, get_openai_client


def reviewer_brief_audio(brief_text: str) -> dict:
    client = get_openai_client()
    response = client.audio.speech.create(
        model=DEFAULT_TTS_MODEL,
        voice=DEFAULT_TTS_VOICE,
        input=brief_text,
        format="mp3",
    )
    audio_bytes = response.read()
    return {
        "provider": "OpenAI",
        "model": DEFAULT_TTS_MODEL,
        "voice": DEFAULT_TTS_VOICE,
        "audio_base64": base64.b64encode(audio_bytes).decode("ascii"),
        "mime_type": "audio/mpeg",
    }
