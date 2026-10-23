import os
from google.cloud import speech_v1p1beta1 as speech

def get_speech_client():
    client = speech.SpeechAsyncClient()
    return client

def get_credentials():
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
    return credentials_path