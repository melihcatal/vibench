from google.cloud import speech


def get_speech_client():
    return speech.SpeechClient()
