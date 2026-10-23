from google.cloud.speech import enums
from google.cloud.speech import types

def create_recognition_config(language_code='en-US', sample_rate_hertz=16000):
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
    )
    return config

def create_streaming_config(config):
    streaming_config = types.StreamingRecognitionConfig(config=config, interim_results=True)
    return streaming_config