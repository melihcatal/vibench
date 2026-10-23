from __future__ import annotations

import os

from elevenlabs import ElevenLabs


ELEVENLABS_MODEL = "eleven_multilingual_v2"
ELEVENLABS_VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"


def generate_reviewer_brief_audio(text: str) -> bytes:
    api_key = os.getenv("ELEVENLABS_API_KEY", "")
    if not api_key:
        raise ValueError("Missing ELEVENLABS_API_KEY")
    client = ElevenLabs(api_key=api_key)
    audio = client.text_to_speech.convert(
        voice_id=ELEVENLABS_VOICE_ID,
        model_id=ELEVENLABS_MODEL,
        text=text,
    )
    if isinstance(audio, bytes):
        return audio
    return b"".join(chunk for chunk in audio)
