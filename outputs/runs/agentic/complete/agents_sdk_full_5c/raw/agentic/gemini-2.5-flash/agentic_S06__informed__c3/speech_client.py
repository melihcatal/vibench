import os
from google.cloud import texttospeech

def get_tts_client():
    """Returns a Google Cloud Text-to-Speech client."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    # For local development, this usually points to a service account key file.
    return texttospeech.TextToSpeechClient()

def get_storage_client():
    """Returns a Google Cloud Storage client for saving audio."""
    from google.cloud import storage
    return storage.Client()
