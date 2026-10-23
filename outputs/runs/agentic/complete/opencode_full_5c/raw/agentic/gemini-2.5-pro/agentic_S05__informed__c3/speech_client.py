import os
from deepgram import DeepgramClient


def get_speech_client():
    api_key = os.getenv("DEEPGRAM_API_KEY")
    if not api_key:
        raise ValueError("DEEPGRAM_API_KEY environment variable not set")
    return DeepgramClient(api_key)
