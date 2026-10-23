from google.cloud import speech_v1p1beta1 as speech
import os

def get_speech_client():
    # Authenticate using GOOGLE_APPLICATION_CREDENTIALS environment variable
    # or relying on default application credentials.
    # For local development, ensure GOOGLE_APPLICATION_CREDENTIALS is set.
    return speech.SpeechClient()
