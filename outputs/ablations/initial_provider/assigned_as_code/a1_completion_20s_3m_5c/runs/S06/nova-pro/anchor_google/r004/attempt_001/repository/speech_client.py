from google.cloud import texttospeech

def get_client():
    return texttospeech.TextToSpeechClient()