from google.cloud.speech_v2 import SpeechClient
from google.auth import load_credentials_from_file
import os

def get_speech_client():
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if credentials_path:
        credentials, _ = load_credentials_from_file(credentials_path)
        return SpeechClient(credentials=credentials)
    return SpeechClient()