import os
from typing import BinaryIO
from elevenlabs.client import ElevenLabs
from elevenlabs.types import VoiceSettings


def generate_platform_brief_audio(text: str) -> bytes:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY required")
    client = ElevenLabs(api_key=api_key)
    voice_id = "21m00Tcm4TlvDq8ikWAM"
    settings = VoiceSettings(
        stability=0.5,
        similarity_boost=0.75,
    )
    audio = client.text_to_speech.convert(
        text=text,
        voice_id=voice_id,
        voice_settings=settings,
        output_format="mp3_44100_128",
    )
    return audio
