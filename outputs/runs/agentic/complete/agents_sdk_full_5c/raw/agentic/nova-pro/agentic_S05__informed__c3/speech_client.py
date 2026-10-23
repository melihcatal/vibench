import os
from google.cloud import speech

# Local configuration and client helper utilities for Streaming Speech-to-Text

def get_speech_client():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your-google-credentials.json'
    return speech.SpeechClient()