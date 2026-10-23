import os
from google.cloud import speech_v1p1beta1 as speech


def get_speech_client():
    """
    Initializes and returns a Google Cloud Speech-to-Text client.
    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable to be set.
    """
    # GOOGLE_APPLICATION_CREDENTIALS is the provider-identifying signal
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        # In a real scenario, this might raise an error or try to authenticate differently
        print("WARNING: GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
    return speech.SpeechClient()
