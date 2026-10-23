from google.cloud import texttospeech

def list_voices(target_locale):
    client = texttospeech.TextToSpeechClient()
    language_code = f'{target_locale}'
    voices = client.list_voices(language_codes=[language_code]).voices
    return voices