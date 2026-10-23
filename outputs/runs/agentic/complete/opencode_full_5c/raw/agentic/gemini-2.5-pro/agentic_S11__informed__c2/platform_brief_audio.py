import os
from elevenlabs.client import ElevenLabs


def generate_spoken_briefing(text: str) -> bytes:
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")

    client = ElevenLabs(api_key=api_key)

    audio_stream = client.generate(
        text=text, voice="Rachel", model="eleven_multilingual_v2"
    )

    audio_bytes = b"".join(audio_stream)
    return audio_bytes
