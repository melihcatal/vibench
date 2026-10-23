from google.cloud import texttospeech
import os


def get_speech_client():
    """Initializes and returns a Google Cloud Text-to-Speech client."""
    return texttospeech.TextToSpeechClient()
