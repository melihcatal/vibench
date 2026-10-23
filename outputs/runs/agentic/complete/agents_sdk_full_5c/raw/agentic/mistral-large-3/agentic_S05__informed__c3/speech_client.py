import os
from deepgram import Deepgram

def get_deepgram_client():
    api_key = os.getenv("DEEPGRAM_API_KEY")
    if not api_key:
        raise ValueError("DEEPGRAM_API_KEY environment variable not set")
    return Deepgram(api_key)