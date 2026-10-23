import os
from google.cloud import speech_v1p1beta1 as speech


def get_speech_client():
    """Initializes and returns a Google Cloud Speech-to-Text client."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or application default credentials are configured.
    # For local development, set GOOGLE_APPLICATION_CREDENTIALS to the path of your service account key file.
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"
    return speech.SpeechClient()


def get_streaming_config(
    language_code: str = "en-US", enable_automatic_punctuation: bool = True
):
    """Returns a StreamingRecognitionConfig for Google Cloud Speech-to-Text."""
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
        model="default",
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )
    return streaming_config
