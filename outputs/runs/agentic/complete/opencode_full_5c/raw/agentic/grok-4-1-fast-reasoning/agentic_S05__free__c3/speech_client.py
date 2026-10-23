import os
from deepgram import DeepgramClient


def get_speech_client() -> DeepgramClient:
    api_key = os.getenv("DEEPGRAM_API_KEY")
    if not api_key:
        raise ValueError("DEEPGRAM_API_KEY environment variable is required")
    return DeepgramClient(api_key)
