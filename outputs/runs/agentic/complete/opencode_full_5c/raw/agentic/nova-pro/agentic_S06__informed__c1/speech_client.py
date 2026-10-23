from google.cloud import texttospeech


def get_texttospeech_client():
    return texttospeech.TextToSpeechClient()
