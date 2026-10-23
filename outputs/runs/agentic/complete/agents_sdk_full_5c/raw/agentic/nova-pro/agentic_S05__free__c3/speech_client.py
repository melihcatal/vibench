from google.cloud import speech
from google.oauth2 import service_account

def create_speech_client():
    credentials = service_account.Credentials.from_service_account_file('path/to/service_account.json')
    client = speech.SpeechClient(credentials=credentials)
    return client