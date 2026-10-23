import os
from google.cloud import speech



def create_speech_client():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/credentials.json"
    return speech.SpeechClient()