import os
from typing import Optional
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs


def generate_spoken_preview(
    text: str,
    voice_id: Optional[str] = "pNInz6obpgDQGcFmaJgB",
    language: Optional[str] = None,
) -> bytes:
    """
    Generates spoken previews of translated copy using ElevenLabs Text to Speech.
    """
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set")

    client = ElevenLabs(api_key=api_key)
    audio = client.generate(
        text=text,
        voice=voice_id,
        model="eleven_multilingual_v2",
        voice_settings=VoiceSettings(stability=0.5, similarity_boost=0.5),
    )
    return b"".join(audio)
