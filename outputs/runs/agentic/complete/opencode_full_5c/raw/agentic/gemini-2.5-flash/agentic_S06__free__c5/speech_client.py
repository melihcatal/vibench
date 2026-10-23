from google.cloud import texttospeech


def get_tts_client():
    """Returns a Google Cloud Text-to-Speech client."""
    return texttospeech.TextToSpeechClient()


def get_default_audio_config():
    """Returns a default audio configuration for Text-to-Speech."""
    return texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16)
