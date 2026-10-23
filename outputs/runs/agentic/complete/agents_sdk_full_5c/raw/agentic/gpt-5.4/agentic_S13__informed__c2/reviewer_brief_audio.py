from __future__ import annotations

import io
import os
from typing import Optional

from elevenlabs.client import ElevenLabs


def reviewer_brief_audio(
    text: str,
    voice_id: str = "JBFqnCBsd6RMkjVDRZzb",
    model_id: str = "eleven_multilingual_v2",
    output_format: str = "mp3_44100_128",
) -> bytes:
    client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])
    audio_stream = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id=model_id,
        output_format=output_format,
        text=text,
    )
    buffer = io.BytesIO()
    for chunk in audio_stream:
        if isinstance(chunk, bytes):
            buffer.write(chunk)
    return buffer.getvalue()
