from typing import List
from elevenlabs import generate, set_api_key
import os


def generate_spoken_preview(text: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM") -> bytes:
    set_api_key(os.getenv("ELEVENLABS_API_KEY"))

    audio = generate(text=text, voice=voice_id, model="eleven_multilingual_v2")

    return audio
