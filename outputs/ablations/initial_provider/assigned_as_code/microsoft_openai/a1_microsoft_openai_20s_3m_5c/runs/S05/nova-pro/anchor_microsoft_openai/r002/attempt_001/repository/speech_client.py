from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

def create_speech_client():
    return speech.SpeechClient()

def normalize_response(response):
    if response.results:
        return [result.alternatives[0].transcript for result in response.results]
    return []