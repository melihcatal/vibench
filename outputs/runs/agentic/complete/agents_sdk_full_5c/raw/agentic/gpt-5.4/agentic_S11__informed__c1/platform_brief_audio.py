from __future__ import annotations

import os
from typing import Any

from elevenlabs import ElevenLabs


DEFAULT_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb")
DEFAULT_MODEL_ID = os.getenv("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2")


def platform_brief_audio(text: str) -> dict[str, Any]:
    client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])
    audio = client.text_to_speech.convert(
        voice_id=DEFAULT_VOICE_ID,
        model_id=DEFAULT_MODEL_ID,
        text=text,
        output_format="mp3_44100_128",
    )
    audio_bytes = b"".join(audio)
    return {
        "audio_bytes": audio_bytes,
        "voice_id": DEFAULT_VOICE_ID,
        "model_id": DEFAULT_MODEL_ID,
        "provider_response": audio,
    }
