import os
from deepgram import DeepgramClient

DEEPGRAM_API_KEY = os.getenv('DEEPGRAM_API_KEY')

def get_stt_client(api_key: str | None = None) -> DeepgramClient:
    key = api_key or DEEPGRAM_API_KEY
    if not key:
        raise ValueError('DEEPGRAM_API_KEY environment variable is required.')
    return DeepgramClient(key)
