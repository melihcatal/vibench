from __future__ import annotations

import os
from typing import BinaryIO

from elevenlabs import generate, set_api_key


TTS_MODEL = "eleven_multilingual_v2"


def generate_platform_brief_audio(text: str) -> bytes:
    set_api_key(os.getenv("ELEVENLABS_API_KEY", ""))
    audio = generate(text=text, model=TTS_MODEL, voice="Rachel")
    return audio
