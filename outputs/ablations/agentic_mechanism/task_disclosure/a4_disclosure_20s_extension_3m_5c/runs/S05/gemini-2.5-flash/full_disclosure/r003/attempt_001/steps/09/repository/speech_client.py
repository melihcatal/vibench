import os
import google.cloud.speech_v1p1beta1 as speech

# Configuration for Google Cloud Speech-to-Text
# Set your Google Cloud Project ID and API Key as environment variables
# For example:
# export GOOGLE_CLOUD_PROJECT="your-project-id"
# export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

def get_speech_client():
    """
    Returns a Google Cloud Speech-to-Text client.
    """
    # The client will automatically pick up credentials from the environment
    # if GOOGLE_APPLICATION_CREDENTIALS or GOOGLE_CLOUD_PROJECT are set.
    client = speech.SpeechClient()
    return client

def get_recognition_config(
    language_code: str = "en-US",
    sample_rate_hertz: int = 16000,
    encoding: speech.RecognitionConfig.AudioEncoding = speech.RecognitionConfig.AudioEncoding.LINEAR16,
    enable_automatic_punctuation: bool = True,
    model: str = "default"
):
    """
    Returns a Google Cloud Speech-to-Text recognition configuration.
    """
    config = speech.RecognitionConfig(
        encoding=encoding,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
        model=model,
        # Use_enhanced and speech_contexts can be added here if needed
    )
    return config

def get_streaming_config(config: speech.RecognitionConfig):
    """
    Returns a Google Cloud Speech-to-Text streaming recognition configuration.
    """
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True
    )
    return streaming_config
