import os
from elevenlabs import ElevenLabs


def get_elevenlabs_client():
    """
    Initializes and returns an ElevenLabs client.
    Requires ELEVENLABS_API_KEY environment variable to be set.
    """
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")
    return ElevenLabs(api_key=api_key)
