from google.cloud import texttospeech

def create_client():
    return texttospeech.TextToSpeechClient()
