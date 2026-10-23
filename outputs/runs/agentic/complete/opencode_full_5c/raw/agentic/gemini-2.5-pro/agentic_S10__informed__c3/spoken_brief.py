import os
from elevenlabs.client import ElevenLabs
from elevenlabs import save


def generate_spoken_brief(text: str, output_path: str):
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")

    client = ElevenLabs(api_key=api_key)

    audio = client.generate(text=text, voice="Rachel", model="eleven_multilingual_v2")

    save(audio, output_path)
