from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from speech_client import create_streaming_client

client = create_streaming_client()
config = types.StreamingRecognitionConfig(config={
    'encoding': enums.RecognitionConfig.AudioEncoding.LINEAR16,
    'sample_rate_hertz': 16000,
    'language_code': 'en-US',
    'enable_automatic_punctuation': True,
}, interim_results=True)

def start_streaming_recognizer():
    return client, config