from google.cloud import texttospeech


def get_text_to_speech_client():
    """Returns a configured Google Cloud Text-to-Speech client."""
    return texttospeech.TextToSpeechClient()
