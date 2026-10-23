from google.cloud.speech import enums
from google.cloud.speech import types

def normalize_response(response):
    return ' '.join([result.alternatives[0].transcript for result in response.results])