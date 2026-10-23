from google.cloud import speech
import os

def get_speech_client():
    """Provides a configured Google Cloud Speech-to-Text client."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # For example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/key.json"
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("Warning: GOOGLE_APPLICATION_CREDENTIALS not set. Using default credentials.")
    return speech.SpeechClient()

def create_streaming_config(
    sampling_rate: int = 16000,
    language_code: str = "en-US",
    enable_automatic_punctuation: bool = True,
    interim_results: bool = True,
) -> speech.StreamingRecognitionConfig:
    """Creates a Google Cloud Speech-to-Text streaming recognition configuration."""
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sampling_rate,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=interim_results
    )
    return streaming_config
