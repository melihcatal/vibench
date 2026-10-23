import os
from deepgram import DeepgramClient

def get_deepgram_client():
    """
    Initializes and returns a DeepgramClient using the API key
    from the DEEPGRAM_API_KEY environment variable.
    """
    api_key = os.getenv("DEEPGRAM_API_KEY")
    if not api_key:
        raise ValueError("DEEPGRAM_API_KEY environment variable not set.")
    
    client = DeepgramClient(api_key)
    return client
