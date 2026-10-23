import os
from deepgram import DeepgramClient

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

def get_deepgram_client():
    if not DEEPGRAM_API_KEY:
        raise ValueError("DEEPGRAM_API_KEY environment variable not set")
    return DeepgramClient(DEEPGRAM_API_KEY)