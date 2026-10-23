import os
from google.cloud import speech_v1p1beta1 as speech
from google.oauth2 import service_account

def get_speech_client():
    """
    Initializes and returns a Google Cloud Speech-to-Text client.
    """
    credentials = service_account.Credentials.from_service_account_file(
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "credentials.json")
    )
    return speech.SpeechClient(credentials=credentials)