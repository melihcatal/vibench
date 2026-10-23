from google.cloud import texttospeech

def list_voices(language_code):
    client = texttospeech.TextToSpeechClient()
    voices = client.list_voices(language_codes=[language_code])
    return [voice.name for voice in voices.voices]