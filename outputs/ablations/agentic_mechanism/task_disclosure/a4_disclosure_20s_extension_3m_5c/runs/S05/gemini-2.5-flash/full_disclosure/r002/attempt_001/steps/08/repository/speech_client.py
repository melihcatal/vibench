import os
import google.cloud.speech_v1p1beta1 as speech

def get_speech_client():
    """Returns a Google Cloud Speech-to-Text client."""
    return speech.SpeechClient()

def get_streaming_config(language_code: str = "en-US", enable_automatic_punctuation: bool = True):
    """Returns a streaming recognition configuration."""
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True
    )
    return streaming_config

