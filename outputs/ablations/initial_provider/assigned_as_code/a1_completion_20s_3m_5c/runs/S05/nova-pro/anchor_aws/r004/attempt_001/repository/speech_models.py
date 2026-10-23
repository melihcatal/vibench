from google.cloud.speech import enums
from google.cloud.speech import types

def create_streaming_config(language_code, enable_automatic_punctuation):
    config = types.StreamingRecognitionConfig(
        config=types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code=language_code,
            enable_automatic_punctuation=enable_automatic_punctuation),
        interim_results=True)
    return config