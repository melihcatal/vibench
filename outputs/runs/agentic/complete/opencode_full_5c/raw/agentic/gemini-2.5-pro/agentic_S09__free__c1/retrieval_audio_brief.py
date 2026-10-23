import os
from elevenlabs import generate, save
from elevenlabs.client import ElevenLabs


def generate_audio_brief(text: str, output_path: str):
    """
    Generates a spoken brief from retrieved search results using ElevenLabs.
    """
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")

    client = ElevenLabs(api_key=api_key)

    audio = client.generate(text=text, voice="Rachel", model="eleven_multilingual_v2")

    with open(output_path, "wb") as f:
        f.write(audio)
