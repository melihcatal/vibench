from google.cloud import texttospeech


def get_client():
    return texttospeech.TextToSpeechClient()


def get_voice_config(language_code, voice_name):
    return texttospeech.VoiceSelectionParams(language_code=language_code, name=voice_name)


def get_audio_config(audio_encoding):
    return texttospeech.AudioConfig(audio_encoding=audio_encoding)
