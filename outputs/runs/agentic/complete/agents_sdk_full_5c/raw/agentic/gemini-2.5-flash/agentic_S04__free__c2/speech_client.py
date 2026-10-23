import os
from google.cloud import speech_v1p1beta1 as speech

def get_speech_client():
    """Initializes and returns a Google Cloud Speech-to-Text client."""
    # Authenticates using credentials in the GOOGLE_APPLICATION_CREDENTIALS environment variable.
    # For local development, set this environment variable or use `gcloud auth application-default login`.
    return speech.SpeechClient()
