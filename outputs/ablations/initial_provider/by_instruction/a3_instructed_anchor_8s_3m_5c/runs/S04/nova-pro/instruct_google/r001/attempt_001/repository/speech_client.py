from google.cloud import speech_v1 as speech

def speech_client():
    client = speech.SpeechClient()
    return client