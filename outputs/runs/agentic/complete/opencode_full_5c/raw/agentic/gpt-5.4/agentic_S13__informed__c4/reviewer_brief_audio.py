from __future__ import annotations

import os
from typing import Any

from elevenlabs import ElevenLabs


MODEL = "eleven_multilingual_v2"


def reviewer_brief_audio(text: str, voice_id: str) -> dict[str, Any]:
    client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])
    audio = client.text_to_speech.convert(voice_id=voice_id, model_id=MODEL, text=text)
    chunks = list(audio)
    audio_bytes = b"".join(chunks)
    return {
        "provider": "elevenlabs",
        "model": MODEL,
        "voice_id": voice_id,
        "audio_bytes": audio_bytes,
        "content_type": "audio/mpeg",
    }
