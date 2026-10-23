from google.cloud import speech
from google.cloud.speech import enums

def create_streaming_config(language_code='en-US'):
    return {
        'encoding': enums.RecognitionConfig.AudioEncoding.LINEAR16,
        'sample_rate_hertz': 16000,
        'language_code': language_code,
    }