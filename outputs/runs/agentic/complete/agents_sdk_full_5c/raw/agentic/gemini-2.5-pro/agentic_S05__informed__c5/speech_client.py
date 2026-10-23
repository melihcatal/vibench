import os
from deepgram import DeepgramClient
from dotenv import load_dotenv

def get_speech_client() -> DeepgramClient:
    """
    Initializes and returns a Deepgram client configured with API key.
    """
    load_dotenv()
    api_key = os.getenv("DEEPGRAM_API_KEY")
    if not api_key:
        raise ValueError("DEEPGRAM_API_KEY environment variable not set.")
    
    client = DeepgramClient(api_key)
    return client
