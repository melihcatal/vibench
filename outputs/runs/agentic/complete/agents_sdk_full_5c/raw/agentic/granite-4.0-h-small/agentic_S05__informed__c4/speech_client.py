# [HELPER] speech_client.py
# Local configuration and helper utilities for Google Cloud Speech-to-Text streaming
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums
import os

# Provider identifier
PROVIDER = "google"

# Environment variable names
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

 def create_speech_client() -> speech.SpeechClient:
    """Create and return a configured SpeechClient."""
    if not PROJECT_ID:
        raise RuntimeError("Set GOOGLE_CLOUD_PROJECT environment variable")
    if not CREDENTIALS_PATH:
        raise RuntimeError("Set GOOGLE_APPLICATION_CREDENTIALS environment variable")
    client = speech.SpeechClient()
    return client

 def build_config(language_code: str = "en-US", enable_automatic_punctuation: bool = True) -> speech.RecognitionConfig:
    """Build a StreamingRecognitionConfig object with the given language and punctuation settings."""
    return speech.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
    )

if __name__ == "__main__":
    client = create_speech_client()
    config = build_config(language_code="es-ES", enable_automatic_punctuation=True)
    print("Client and config ready for streaming:", config)