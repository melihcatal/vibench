import os
from elevenlabs.client import ElevenLabsClient


def generate_speech(text: str) -> bytes:
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")

    client = ElevenLabsClient(api_key=api_key)

    audio = client.generate(text=text, voice="Rachel", model="eleven_multilingual_v2")

    return b"".join(audio)
