import os
from google.cloud import texttospeech


def get_tts_client():
    """Initializes and returns a Google Cloud Text-to-Speech client."""
    # Instantiates a client. Expects GOOGLE_APPLICATION_CREDENTIALS env var.
    return texttospeech.TextToSpeechClient()


def get_project_id():
    """Retrieves the GCP project ID from environment variables."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
    return project_id
