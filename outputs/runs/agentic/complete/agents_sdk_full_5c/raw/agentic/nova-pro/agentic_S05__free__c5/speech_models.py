from google.cloud.speech import enums
from google.cloud.speech import types

def create_config(language_code='en-US'):
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=True,
    )
    return config

def create_streaming_config(config):
    streaming_config = types.StreamingRecognitionConfig(config=config, interim_results=True)
    return streaming_config