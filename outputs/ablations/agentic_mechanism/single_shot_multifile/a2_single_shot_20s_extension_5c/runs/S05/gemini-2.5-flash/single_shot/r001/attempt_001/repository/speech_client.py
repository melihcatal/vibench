from google.cloud import speech_v1p1beta1 as speech

def get_speech_client():
    return speech.SpeechClient()