import os
from google.cloud import speech


def get_speech_client():
    """Provides a configured Google Cloud Speech-to-Text client."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set in the environment
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print(
            "Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable is not set."
        )
        print("Please set it to the path of your service account key file.")
    return speech.SpeechClient()
