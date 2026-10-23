import os
from typing import Optional
from elevenlabs.client import ElevenLabs

def get_speech_client() -> ElevenLabs:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set")
    return ElevenLabs(api_key=api_key)