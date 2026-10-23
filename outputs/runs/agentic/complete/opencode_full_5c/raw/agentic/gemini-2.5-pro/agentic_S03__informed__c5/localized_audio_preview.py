import os
from elevenlabs.client import ElevenLabs


def localized_audio_preview(text: str) -> bytes:
    """
    Generates a spoken preview of translated copy using ElevenLabs.
    """
    client = ElevenLabs(
        api_key=os.environ.get("ELEVENLABS_API_KEY"),
    )

    audio = client.generate(text=text, voice="Rachel", model="eleven_multilingual_v2")

    audio_bytes = b""
    for chunk in audio:
        audio_bytes += chunk

    return audio_bytes
