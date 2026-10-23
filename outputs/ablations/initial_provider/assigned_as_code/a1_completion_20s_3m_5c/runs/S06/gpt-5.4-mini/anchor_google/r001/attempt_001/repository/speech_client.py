from google.cloud import texttospeech


def get_client():
    return texttospeech.TextToSpeechClient()


def audio_encoding(name="MP3"):
    return getattr(texttospeech.AudioEncoding, name)


def normalize_language_code(value, default="en-US"):
    return value or default
