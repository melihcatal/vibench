import os
from google.cloud import speech


def get_speech_client():
    """Returns a Google Cloud Speech-to-Text client."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # For local development, this usually points to a service account key file.
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
        print("Please ensure your Google Cloud authentication is configured.")
    return speech.SpeechClient()
