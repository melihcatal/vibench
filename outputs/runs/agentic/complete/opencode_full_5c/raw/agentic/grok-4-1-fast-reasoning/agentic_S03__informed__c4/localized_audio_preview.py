import os
from elevenlabs.client import ElevenLabs
from typing import Optional


def localized_audio_preview(
    text: str, language_code: str = "en", voice_id: str = "21m00Tcm4TlvDq8ikWAM"
) -> bytes:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable is required.")
    client = ElevenLabs(api_key=api_key)
    audio = client.generate(
        text=text,
        voice=voice_id,
        model="eleven_multilingual_v2",
        language_code=language_code,
        output_format="mp3_22050_32",
    )
    return audio
