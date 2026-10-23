import os
from typing import Optional
from elevenlabs.client import ElevenLabs


def get_tts_client(api_key: Optional[str] = None) -> ElevenLabs:
    if api_key is None:
        api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY must be set in environment variables.")
    return ElevenLabs(api_key=api_key)
