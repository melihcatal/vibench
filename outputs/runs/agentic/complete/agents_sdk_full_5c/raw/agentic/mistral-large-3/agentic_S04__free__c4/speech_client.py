import os
from google.cloud import speech_v2 as speech
from google.auth import load_credentials_from_file

def get_speech_client() -> speech.SpeechClient:
    """Initialize and return a Google Cloud Speech-to-Text client."""
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if credentials_path:
        credentials, _ = load_credentials_from_file(credentials_path)
        return speech.SpeechClient(credentials=credentials)
    return speech.SpeechClient()