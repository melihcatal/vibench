from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types


def create_streaming_recognizer(language_code="en-US"):
    client = speech.SpeechClient()
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=True,
    )
    streaming_config = types.StreamingRecognitionConfig(config=config)
    return client, streaming_config
