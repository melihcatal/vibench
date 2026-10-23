# [HELPER] speech_client.py

from google.cloud import speech_v1p1beta1 as speech

# Identify provider: Google Cloud Speech-to-Text


def create_speech_client():
    return speech.SpeechClient()


# Optionally set GOOGLE_APPLICATION_CREDENTIALS env variable before calling this function.
