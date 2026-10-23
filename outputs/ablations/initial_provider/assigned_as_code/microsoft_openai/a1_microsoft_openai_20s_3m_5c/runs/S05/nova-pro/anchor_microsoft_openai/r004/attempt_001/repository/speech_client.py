from google.cloud import speech_v1 as speech
from google.cloud.speech_v1 import enums

def create_speech_client():
    return speech.SpeechClient()

def create_streaming_config(language_code='en-US', enable_automatic_punctuation=True):
    return {
        'encoding': enums.RecognitionConfig.AudioEncoding.LINEAR16,
        'sample_rate_hertz': 16000,
        'language_code': language_code,
        'enable_automatic_punctuation': enable_automatic_punctuation,
    }