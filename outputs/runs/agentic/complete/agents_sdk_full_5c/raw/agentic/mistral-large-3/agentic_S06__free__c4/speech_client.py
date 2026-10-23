import os
from google.cloud import texttospeech_v1
from google.oauth2 import service_account


def get_speech_client() -> texttospeech_v1.TextToSpeechClient:
    """Initialize and return a Google Cloud Text-to-Speech client."""
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if credentials_path:
        credentials = service_account.Credentials.from_service_account_file(credentials_path)
        return texttospeech_v1.TextToSpeechClient(credentials=credentials)
    
    return texttospeech_v1.TextToSpeechClient()