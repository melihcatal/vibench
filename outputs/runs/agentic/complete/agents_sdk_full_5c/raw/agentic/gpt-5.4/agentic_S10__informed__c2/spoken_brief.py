from __future__ import annotations

import os

from elevenlabs import ElevenLabs

from model_models import SpeechResult

DEFAULT_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb")
DEFAULT_MODEL_ID = os.getenv("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2")


def generate_spoken_brief(text: str, *, voice_id: str = DEFAULT_VOICE_ID, model_id: str = DEFAULT_MODEL_ID) -> SpeechResult:
    client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id=model_id,
        text=text,
    )
    audio_bytes = b"".join(audio)
    return SpeechResult(audio_bytes=audio_bytes, content_type="audio/mpeg", raw=None)
