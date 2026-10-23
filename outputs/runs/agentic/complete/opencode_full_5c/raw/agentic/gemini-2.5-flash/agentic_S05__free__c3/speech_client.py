import os
from google.cloud import speech_v1p1beta1 as speech


def get_speech_client():
    """Returns a Google Cloud Speech-to-Text client."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set for authentication
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        # This is a placeholder for local development without explicit auth setup.
        # In production, ensure proper authentication is configured.
        pass
    return speech.SpeechClient()


def get_streaming_config(language_code="en-US", enable_automatic_punctuation=True):
    """Returns a Google Cloud Speech-to-Text streaming recognition config."""
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
        model="latest_long",  # Provider-specific model ID
        use_enhanced=True,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )
    return streaming_config
