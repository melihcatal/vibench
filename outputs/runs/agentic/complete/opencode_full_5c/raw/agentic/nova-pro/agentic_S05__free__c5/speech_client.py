import os
from google.cloud import speech_v1 as speech


def get_speech_client():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
        "path/to/your-google-credentials.json"
    )
    return speech.SpeechClient()
