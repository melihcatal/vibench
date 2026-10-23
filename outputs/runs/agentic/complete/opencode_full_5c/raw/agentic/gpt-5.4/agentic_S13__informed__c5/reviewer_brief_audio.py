from __future__ import annotations

import os

from elevenlabs.client import ElevenLabs


def reviewer_brief_audio(text: str, voice_id: str = "JBFqnCBsd6RMkjVDRZzb") -> bytes:
    client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])
    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        output_format="mp3_44100_128",
        model_id="eleven_multilingual_v2",
        text=text,
    )
    return b"".join(audio)
