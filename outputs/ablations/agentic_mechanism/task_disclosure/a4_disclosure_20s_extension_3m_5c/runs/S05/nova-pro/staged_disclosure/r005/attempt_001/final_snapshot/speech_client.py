from google.cloud import speech_v1 as speech
from google.cloud.speech_v1 import enums
from google.cloud.speech_v1 import types

def create_speech_client():
    return speech.SpeechClient()

def create_streaming_config(language_code):
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
    )
    streaming_config = types.StreamingRecognitionConfig(config=config, interim_results=True)
    return streaming_config