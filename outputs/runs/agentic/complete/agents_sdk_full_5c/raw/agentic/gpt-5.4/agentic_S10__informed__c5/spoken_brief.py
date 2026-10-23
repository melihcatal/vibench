from __future__ import annotations

import os
from typing import Optional

from elevenlabs.client import ElevenLabs


DEFAULT_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb")
DEFAULT_MODEL_ID = os.getenv("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2")


def generate_spoken_brief(text: str, output_path: str, voice_id: Optional[str] = None) -> str:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise RuntimeError("ELEVENLABS_API_KEY is required")
    client = ElevenLabs(api_key=api_key)
    audio = client.text_to_speech.convert(
        voice_id=voice_id or DEFAULT_VOICE_ID,
        model_id=DEFAULT_MODEL_ID,
        text=text,
    )
    with open(output_path, "wb") as file_obj:
        for chunk in audio:
            file_obj.write(chunk)
    return output_path
