import os
from google.cloud import speech


def get_speech_client():
    """Returns a Google Cloud Speech-to-Text client."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        # In a real application, you might raise an error or handle this more gracefully.
        # For this example, we'll assume it's set or rely on default ADC.
        print(
            "WARNING: GOOGLE_APPLICATION_CREDENTIALS not set. Relying on default application credentials."
        )
    return speech.SpeechClient()


def get_recognition_config(
    sample_rate_hertz=16000, language_code="en-US", enable_automatic_punctuation=True
):
    """Returns a Google Cloud Speech RecognitionConfig."""
    return speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,  # Assuming LINEAR16, adjust if needed
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
    )


def get_streaming_config(config, interim_results=True):
    """Returns a Google Cloud Speech StreamingRecognitionConfig."""
    return speech.StreamingRecognitionConfig(
        config=config,
        interim_results=interim_results,
    )
