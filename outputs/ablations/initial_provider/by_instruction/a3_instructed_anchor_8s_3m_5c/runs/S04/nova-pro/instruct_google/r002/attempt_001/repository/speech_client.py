from google.cloud import speech_v1 as speech

def speech_client():
    return speech.SpeechClient()