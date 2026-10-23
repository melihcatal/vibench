from elevenlabs import generate, set_api_key
import os

def generate_audio_brief(text: str, voice: str = "Rachel") -> bytes:
    set_api_key(os.getenv("ELEVENLABS_API_KEY"))
    audio = generate(text=text, voice=voice, model="eleven_multilingual_v2")
    return audio