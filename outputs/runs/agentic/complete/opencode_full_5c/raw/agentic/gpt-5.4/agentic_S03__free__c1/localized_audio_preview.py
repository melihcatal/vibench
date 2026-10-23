from __future__ import annotations

import os

from elevenlabs import ElevenLabs


ELEVENLABS_MODEL_ID = "eleven_multilingual_v2"


def localized_audio_preview(text: str, voice_id: str = "JBFqnCBsd6RMkjVDRZzb") -> bytes:
    client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id=ELEVENLABS_MODEL_ID,
        text=text,
    )
    return b"".join(audio)
