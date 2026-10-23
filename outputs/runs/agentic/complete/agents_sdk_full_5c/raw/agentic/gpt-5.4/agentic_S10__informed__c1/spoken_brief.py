from __future__ import annotations

import os

from elevenlabs.client import ElevenLabs


DEFAULT_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb")
DEFAULT_MODEL_ID = os.getenv("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2")


def generate_spoken_brief(text: str) -> bytes:
    client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
    audio = client.text_to_speech.convert(
        voice_id=DEFAULT_VOICE_ID,
        model_id=DEFAULT_MODEL_ID,
        text=text,
        output_format="mp3_44100_128",
    )
    return b"".join(audio)
