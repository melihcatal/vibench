import os
from dotenv import load_dotenv
from elevenlabs import play
from elevenlabs.client import ElevenLabs

load_dotenv()


def generate_spoken_brief_elevenlabs(text: str, voice: str = "Adam"):
    """
    Generates a spoken brief from the model output using ElevenLabs.
    """
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY not found in environment variables.")

    client = ElevenLabs(api_key=api_key)

    audio = client.generate(text=text, voice=voice, model="eleven_multilingual_v2")

    return audio
