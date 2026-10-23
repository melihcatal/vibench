import os
from elevenlabs.client import ElevenLabs


def generate_spoken_brief(text: str) -> bytes:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable is required")
    client = ElevenLabs(api_key=api_key)
    audio = client.generate(
        text=text,
        voice="21m00Tcm4TlvDq8ikWAM",
        model="eleven_monolingual_v1",
        output_format="mp3_22050_32",
    )
    return audio
