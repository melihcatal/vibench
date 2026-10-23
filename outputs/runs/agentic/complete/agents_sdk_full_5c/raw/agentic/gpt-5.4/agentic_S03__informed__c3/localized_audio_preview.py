from __future__ import annotations

import os
from typing import Optional

from elevenlabs import ElevenLabs



def localized_audio_preview(
    text: str,
    voice_id: str,
    model_id: str = "eleven_multilingual_v2",
    output_format: str = "mp3_44100_128",
    language_code: Optional[str] = None,
) -> bytes:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY is required")
    client = ElevenLabs(api_key=api_key)
    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id=model_id,
        output_format=output_format,
        text=text,
        language_code=language_code,
    )
    return b"".join(audio)
