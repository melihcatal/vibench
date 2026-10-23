from __future__ import annotations

import os

from elevenlabs import ElevenLabs

VOICE_ID = "Rachel"
MODEL_ID = "eleven_multilingual_v2"


def localized_audio_preview(text: str) -> bytes:
    client = ElevenLabs(api_key=os.environ.get("ELEVENLABS_API_KEY", ""))
    audio = client.text_to_speech.convert(voice_id=VOICE_ID, model_id=MODEL_ID, text=text)
    return b"".join(audio)
