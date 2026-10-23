import os

from google.cloud import speech_v1p1beta1 as speech


def get_speech_client():
    """Provides a Google Cloud Speech-to-Text client instance."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or authentication is handled implicitly by the Google Cloud SDK.
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
        print("Please set it to the path of your service account key file.")

    return speech.SpeechClient()


def get_streaming_config(
    language_code: str = "en-US", enable_automatic_punctuation: bool = True
):
    """Provides a default streaming recognition configuration."""
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,  # Assuming a common sample rate
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
        model="default",
        use_enhanced=True,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )
    return streaming_config
