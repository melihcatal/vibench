from google.cloud import speech_v1p1beta1 as speech
import os

def get_speech_client():
    """Provides a Google Cloud Speech-to-Text client."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or authenticate using other methods as per Google Cloud SDK documentation.
    return speech.SpeechClient()
