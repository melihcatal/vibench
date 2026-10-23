import os
from deepgram import DeepgramClient

def get_speech_client() -> DeepgramClient:
    """

    Initializes and returns the Deepgram client using the API key
    from the environment variables.

    Raises:
        ValueError: If the DEEPGRAM_API_KEY environment variable is not set.

    Returns:
        DeepgramClient: An initialized Deepgram client.
    """
    api_key = os.getenv("DEEPGRAM_API_KEY")
    if not api_key:
        raise ValueError("DEEPGRAM_API_KEY environment variable not set.")
    
    client = DeepgramClient(api_key)
    return client
