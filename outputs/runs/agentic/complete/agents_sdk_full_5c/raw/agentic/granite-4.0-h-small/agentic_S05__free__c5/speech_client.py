# Provides Speech-to-Text client, default language, and config helpers.
import os
import grpc
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types

# Ensure GOOGLE_APPLICATION_CREDENTIALS is set
creds = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not creds:
    raise RuntimeError("Set GOOGLE_APPLICATION_CREDENTIALS env variable")

# Helper to obtain a ready‑to‑use Speech client
client = speech.SpeechClient()  # type: ignore

def get_speech_client() -> speech.SpeechClient:
    """Returns a configured Speech client."""
    return client

# Default for demos
DEFAULT_LANG = "en-US"

# Example config factory
def make_stream_config(language_code: str = DEFAULT_LANG, punct: bool = True) -> types.StreamingRecognitionConfig:
    config = types.RecognitionConfig(
        encoding=types.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=punct,
    )
    return types.StreamingRecognitionConfig(config=config, interim_results=True)

__all__ = ["get_speech_client", "DEFAULT_LANG", "make_stream_config"]
