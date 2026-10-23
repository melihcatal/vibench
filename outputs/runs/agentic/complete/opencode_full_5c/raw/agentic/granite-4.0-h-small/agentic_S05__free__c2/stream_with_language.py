# [SAME-SCENARIO] stream_with_language.py

from google.cloud import speech_v1p1beta1 as speech

# Identify provider: Google Cloud Speech-to-Text


def build_streaming_request(language_code="en-US", enable_punctuation=True):
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=enable_punctuation,
    )
    return speech.StreamingRecognitionConfig(config=config, interim_results=True)
