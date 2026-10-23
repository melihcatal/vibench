import os
import elevenlabs
from typing import Any

def platform_brief_audio(text: str, voice: str = "Rachel", model: str = "eleven_monolingual_v1") -> bytes:
    elevenlabs.set_api_key(os.getenv("ELEVENLABS_API_KEY"))
    audio = elevenlabs.generate(
        text=text,
        voice=voice,
        model=model
    )
    return audio
