import os
from google.cloud import speech


def get_speech_client():
    """Initializes and returns a Google Cloud Speech-to-Text client."""
    return speech.SpeechClient()


def get_gcs_uri(bucket_name, file_name):
    """Constructs a Google Cloud Storage URI."""
    return f"gs://{bucket_name}/{file_name}"
