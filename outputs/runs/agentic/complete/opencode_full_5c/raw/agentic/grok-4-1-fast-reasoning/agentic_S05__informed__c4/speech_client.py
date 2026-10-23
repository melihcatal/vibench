import os
from deepgram import DeepgramClient

def get_stt_client() -&gt; DeepgramClient:
    api_key = os.getenv('DEEPGRAM_API_KEY')
    if not api_key:
        raise ValueError('DEEPGRAM_API_KEY must be set')
    return DeepgramClient(api_key)