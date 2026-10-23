from google.cloud import texttospeech

def get_tts_client():
    return texttospeech.TextToSpeechClient()