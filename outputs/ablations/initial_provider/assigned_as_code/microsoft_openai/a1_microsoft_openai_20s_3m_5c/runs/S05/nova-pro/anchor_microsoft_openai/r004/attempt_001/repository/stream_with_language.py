from google.cloud import speech_v1 as speech
from google.cloud.speech_v1 import enums

def start_streaming_recognizer(language_code='en-US', enable_automatic_punctuation=True):
    client = speech.SpeechClient()
    config = {
        'encoding': enums.RecognitionConfig.AudioEncoding.LINEAR16,
        'sample_rate_hertz': 16000,
        'language_code': language_code,
        'enable_automatic_punctuation': enable_automatic_punctuation,
    }
    return client, config