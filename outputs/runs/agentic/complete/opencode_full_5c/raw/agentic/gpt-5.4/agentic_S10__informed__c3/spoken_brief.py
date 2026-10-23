from __future__ import annotations

import os

from elevenlabs.client import ElevenLabs


def generate_spoken_brief(text: str, voice_id: str = "JBFqnCBsd6RMkjVDRZzb") -> bytes:
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY is required")
    client = ElevenLabs(api_key=api_key)
    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id="eleven_multilingual_v2",
        text=text,
        output_format="mp3_44100_128",
    )
    return b"".join(audio)
