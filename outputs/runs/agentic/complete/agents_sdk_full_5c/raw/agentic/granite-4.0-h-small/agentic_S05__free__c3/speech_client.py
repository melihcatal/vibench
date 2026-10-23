import os
from google.cloud import speech_v1p1beta1 as speech

# ---------------------------------------------------------------------------
# HELPER: speech_client.py                                                 #
# Provides a thin wrapper to create a Google Cloud Speech client with
# default credentials and common configuration helpers.
# ---------------------------------------------------------------------------

def get_speech_client() -> speech.SpeechClient:
    """
    Returns an authenticated SpeechClient.

    The client reads credentials from the environment (e.g., GOOGLE_APPLICATION_CREDENTIALS)
    or uses Application Default Credentials.
    """
    return speech.SpeechClient()

# Example helper: construct default recognition config
# (duplicate code can be moved here if shared across modules)
def default_recognition_config() -> speech.RecognitionConfig:
    return speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_automatic_punctuation=True,
    )
