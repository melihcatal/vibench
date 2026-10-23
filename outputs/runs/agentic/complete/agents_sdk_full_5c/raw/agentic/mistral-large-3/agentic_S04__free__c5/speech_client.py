import os
from google.cloud import speech_v2 as speech

def get_speech_client() -> speech.SpeechClient:
    """Initialize and return a Google Cloud Speech-to-Text client."""
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
    
    return speech.SpeechClient()