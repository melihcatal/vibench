import os
from elevenlabs import generate, play, set_api_key
from dotenv import load_dotenv

load_dotenv()


def generate_spoken_brief(text: str):
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")
    set_api_key(api_key)

    audio = generate(text=text, voice="Rachel", model="eleven_multilingual_v2")

    return audio
