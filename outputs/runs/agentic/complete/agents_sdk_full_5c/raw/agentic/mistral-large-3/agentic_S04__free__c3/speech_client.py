import os
from google.cloud import speech_v2 as speech
from google.oauth2 import service_account

def get_speech_client() -> speech.SpeechClient:
    """Initialize and return a Google Cloud Speech-to-Text client."""
    credentials = service_account.Credentials.from_service_account_file(
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    )
    return speech.SpeechClient(credentials=credentials)