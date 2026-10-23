import os
from typing import Optional
from elevenlabs.client import ElevenLabs


def generate_spoken_preview(
    text: str, voice: str = "Rachel", model_id: str = "eleven_multilingual_v2"
) -> bytes:
    client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
    audio = client.generate(text=text, voice=voice, model=model_id)
    return audio
