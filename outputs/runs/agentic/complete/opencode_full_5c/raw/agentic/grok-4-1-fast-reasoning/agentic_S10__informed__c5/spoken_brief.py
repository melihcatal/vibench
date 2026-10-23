import os
from elevenlabs import generate, set_api_key


def spoken_brief(text: str, voice: str = "Rachel") -> bytes:
    set_api_key(os.getenv("ELEVENLABS_API_KEY"))
    audio = generate(text=text, voice=voice, model="eleven_monolingual_v1")
    return audio
