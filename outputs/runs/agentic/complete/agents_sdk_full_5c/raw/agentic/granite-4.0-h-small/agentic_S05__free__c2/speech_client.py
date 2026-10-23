import os
import google.cloud.speech_v1 as speech
from google.cloud.speech_v1 import enums

# Provider-specific credentials handling
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', './service_account.json')

session_client = speech.SpeechClient()


def get_stt_client():
    """
    Returns a configured streaming speech-to-text client.
    """
    client = session_client
    return client


def get_config(language_code='en-US', enable_automatic_punctuation=True):
    """
    Builds a streaming recognition config with optional punctuation.
    """
    return speech.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
        model='default'  # Provider-specific model identifier
    )