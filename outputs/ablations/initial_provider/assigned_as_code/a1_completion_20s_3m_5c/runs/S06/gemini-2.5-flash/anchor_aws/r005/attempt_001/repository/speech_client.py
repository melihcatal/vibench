from google.cloud import texttospeech
import os

def get_text_to_speech_client():
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or use default client which automatically finds credentials
    # For local development, set GOOGLE_APPLICATION_CREDENTIALS to the path of your service account key file.
    # Example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
    return texttospeech.TextToSpeechClient()
