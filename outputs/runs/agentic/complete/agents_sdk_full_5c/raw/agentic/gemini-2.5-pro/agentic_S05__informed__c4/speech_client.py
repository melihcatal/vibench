import os
from deepgram import DeepgramClient, DeepgramClientOptions

def get_speech_client():
    """Initializes and returns the Deepgram client."""
    api_key = os.getenv("DEEPGRAM_API_KEY")
    if not api_key:
        raise ValueError("DEEPGRAM_API_KEY environment variable not set.")
    
    config = DeepgramClientOptions(
        verbose=0, # Suppress verbose logging
    )
    
    deepgram = DeepgramClient(api_key, config)
    return deepgram
