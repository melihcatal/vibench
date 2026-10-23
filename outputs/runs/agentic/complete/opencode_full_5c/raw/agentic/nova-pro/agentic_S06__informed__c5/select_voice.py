import os
from elevenlabs import Client, Voice


def select_voice() -> list:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    client = Client(api_key=api_key)
    voices = client.voices()
    return voices
