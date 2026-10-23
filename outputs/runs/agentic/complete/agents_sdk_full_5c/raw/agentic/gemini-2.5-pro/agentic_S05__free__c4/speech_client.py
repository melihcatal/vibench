import os
from google.cloud import speech

def get_speech_client():
    """Initializes and returns a Google Cloud Speech-to-Text client."""
    # Instantiates a client. Credentials will be automatically found
    # if the GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    return speech.SpeechClient()

# Common audio configuration
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms
