import os
from google.cloud import speech

def get_speech_client():
    """Provides a Google Cloud Speech-to-Text client."""
    return speech.SpeechClient()

def get_streaming_config(language_code: str, sample_rate_hertz: int, enable_automatic_punctuation: bool = False):
    """
    Returns a Google Cloud Speech-to-Text streaming recognition configuration.
    """
    return speech.StreamingRecognitionConfig(
        config=speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=sample_rate_hertz,
            language_code=language_code,
            enable_automatic_punctuation=enable_automatic_punctuation,
        ),
        interim_results=True,
    )
