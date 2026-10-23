from google.cloud import texttospeech
import os

def get_text_to_speech_client() -> texttospeech.TextToSpeechClient:
    """Provides a Google Cloud Text-to-Speech client."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set in the environment
    # For example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
    return texttospeech.TextToSpeechClient()

