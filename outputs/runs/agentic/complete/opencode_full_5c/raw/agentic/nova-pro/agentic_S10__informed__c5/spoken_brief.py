import os
from elevenlabs import voices, text_to_speech


def generate_spoken_brief(text):
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set")
    audio = text_to_speech(text, voice=voices.Rachel)
    return audio
