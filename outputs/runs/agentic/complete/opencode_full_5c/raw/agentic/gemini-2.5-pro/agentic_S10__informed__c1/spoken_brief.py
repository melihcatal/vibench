import os
from elevenlabs.client import ElevenLabs


def generate_spoken_brief(text: str) -> bytes:
    """
    Generate a spoken brief from the model output using ElevenLabs API.
    """
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")

    client = ElevenLabs(api_key=api_key)

    try:
        audio = client.generate(
            text=text, voice="Rachel", model="eleven_multilingual_v2"
        )

        audio_bytes = b"".join(audio)
        return audio_bytes

    except Exception as e:
        print(f"ElevenLabs API error: {e}")
        return b""
