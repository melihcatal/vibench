import os
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

load_dotenv()


def generate_audio_brief(text: str, output_path: str = "retrieval_brief.mp3"):
    """
    Generate a spoken brief from retrieved search results using ElevenLabs API.
    """
    api_key = os.getenv("ELEVEN_API_KEY")
    if not api_key:
        raise ValueError("ELEVEN_API_KEY environment variable not set.")

    client = ElevenLabs(api_key=api_key)

    audio = client.generate(text=text, voice="Rachel", model="eleven_multilingual_v2")

    with open(output_path, "wb") as f:
        f.write(audio)

    return output_path
