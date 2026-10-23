# speech_client.py
import os
from google.cloud import texttospeech


def get_client():
    """Return a configured Text-to-Speech client using GOOGLE_APPLICATION_CREDENTIALS env var."""
    return texttospeech.TextToSpeechClient()


def configure_credentials(credentials_path=None):
    """Set GOOGlE_APPLICATION_CREDENTIALS if not already set."""
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS") and credentials_path:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
