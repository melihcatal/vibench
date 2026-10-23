import os
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums

# Load credentials from environment (default behavior for GCP client library)
# GOOGLE_APPLICATION_CREDENTIALS env var points to a JSON key file.

# Helper singleton client factory
_speech_client = None

def get_speech_client():
    """Return a configured Speech-to-Text client, lazily initialized."""
    global _speech_client
    if _speech_client is None:
        _speech_client = speech.SpeechClient()
    return _speech_client

# Optional helper to build config with defaults

def build_recognition_config(
    language_code: str = "en-US",
    sample_rate_hertz: int = 16000,
    enable_automatic_punctuation: bool = True,
    speech_contexts=None,
    enable_word_time_offsets: bool = False,
):
    """Create a standard RecognitionConfig object."""
    return speech.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
        speech_contexts=speech_contexts or [],
        enable_word_time_offsets=enable_word_time_offsets,
    )

# Example of using the generated config elsewhere:
# config = build_recognition_config(language_code="es-ES", sample_rate_hertz=22050)
