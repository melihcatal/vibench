from google.cloud import texttospeech

def select_voice(language_code):
    client = texttospeech.TextToSpeechClient()
    voices = client.list_voices(language_code=language_code).voices
    return voices