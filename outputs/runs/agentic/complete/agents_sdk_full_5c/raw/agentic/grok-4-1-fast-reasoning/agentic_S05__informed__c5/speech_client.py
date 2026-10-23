import os
from deepgram import DeepgramClient

_client = None

def get_speech_client():
    global _client
    if _client is None:
        api_key = os.getenv('DEEPGRAM_API_KEY')
        if not api_key:
            raise ValueError("DEEPGRAM_API_KEY environment variable is required.")
        _client = DeepgramClient(api_key)
    return _client
