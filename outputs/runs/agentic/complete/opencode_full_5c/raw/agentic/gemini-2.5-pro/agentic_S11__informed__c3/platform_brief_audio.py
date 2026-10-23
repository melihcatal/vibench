import os
from elevenlabs.client import ElevenLabs


def generate_audio_briefing(text: str, output_path: str):
    """
    Generates a spoken briefing from platform outputs using ElevenLabs.

    Args:
        text: The text to convert to speech.
        output_path: The path to save the generated audio file.
    """
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable is not set.")

    client = ElevenLabs(api_key=api_key)

    audio = client.generate(text=text, voice="Rachel", model="eleven_multilingual_v2")

    with open(output_path, "wb") as f:
        f.write(audio)

    return output_path
