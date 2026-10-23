import os
from google.cloud import speech

def get_speech_client():
    """Initializes and returns a Google Cloud Speech client."""
    # This will use the credentials set up in the environment,
    # e.g., via `gcloud auth application-default login`
    return speech.SpeechClient()

def get_streaming_config(
    sample_rate_hertz=16000, language_code="en-US", interim_results=False, punctuation=False
):
    """Returns a streaming recognition config."""
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        enable_automatic_punctuation=punctuation,
        model="latest_long",
    )
    return speech.StreamingRecognitionConfig(
        config=config, interim_results=interim_results
    )
