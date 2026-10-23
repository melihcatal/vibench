import os
from elevenlabs import generate, set_api_key
from typing import Iterator


def generate_audio_briefing(text: str) -> Iterator[bytes]:
    """
    Generates a spoken briefing from platform output using ElevenLabs API.
    """
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")
    set_api_key(api_key)

    audio_stream = generate(
        text=text, voice="Rachel", model="eleven_multilingual_v2", stream=True
    )

    return audio_stream
