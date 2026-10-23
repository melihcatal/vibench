import os
from elevenlabs import Client


def get_speech_client() -> Client:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    return Client(api_key=api_key)
