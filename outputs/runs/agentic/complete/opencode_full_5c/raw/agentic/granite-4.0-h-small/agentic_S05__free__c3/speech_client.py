import os
from google.cloud import speech_v1p1beta1 as speech


def get_client():
    """
    Helper to obtain a SpeechClient instance.
    Uses GOOGLE_APPLICATION_CREDENTIALS environment variable to load credentials.
    """
    # concrete GCP provider
    return speech.SpeechClient()


def load_credentials():
    """
    Load credentials from environment variable for local configuration.
    Returns path to credentials file or raises if missing.
    """
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise RuntimeError(
            "Set GOOGLE_APPLICATION_CREDENTIALS to point to service account JSON"
        )
    return credentials_path
