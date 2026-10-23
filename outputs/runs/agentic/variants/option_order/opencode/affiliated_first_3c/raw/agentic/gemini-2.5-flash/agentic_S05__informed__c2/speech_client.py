import os
from google.cloud import speech


def get_streaming_speech_client():
    """Returns a Google Cloud Speech-to-Text client."""
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    # to the path of your service account key file.
    # For example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/key.json"
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        print(
            "WARNING: GOOGLE_APPLICATION_CREDENTIALS environment variable not set. "
            "Streaming speech recognition may fail if not authenticated."
        )
    return speech.SpeechClient()
