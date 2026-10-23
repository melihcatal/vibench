from google.cloud import texttospeech


def get_tts_client():
    """Initializes and returns a TextToSpeechClient."""
    return texttospeech.TextToSpeechClient()
