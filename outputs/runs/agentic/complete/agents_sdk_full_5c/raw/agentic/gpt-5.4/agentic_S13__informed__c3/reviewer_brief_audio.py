from __future__ import annotations

import os

from elevenlabs.client import ElevenLabs


VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"
MODEL_ID = "eleven_multilingual_v2"


def generate_reviewer_brief_audio(text: str) -> bytes:
    client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])
    audio = client.text_to_speech.convert(
        voice_id=VOICE_ID,
        model_id=MODEL_ID,
        text=text,
        output_format="mp3_44100_128",
    )
    return b"".join(audio) if not isinstance(audio, (bytes, bytearray)) else bytes(audio)
