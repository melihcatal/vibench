import os
from elevenlabs.client import ElevenLabs
from typing import Optional


def retrieval_audio_brief(brief_text: str, voice: str = "Rachel") -> bytes:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY not set")
    client = ElevenLabs(api_key=api_key)
    audio = client.generate(text=brief_text, voice=voice, model="eleven_monolingual_v1")
    return audio
