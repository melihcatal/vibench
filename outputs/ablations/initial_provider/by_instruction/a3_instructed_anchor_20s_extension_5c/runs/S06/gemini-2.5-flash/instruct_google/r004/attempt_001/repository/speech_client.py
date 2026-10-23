from google.cloud import texttospeech

def get_tts_client():
    """Initializes and returns a Google Cloud Text-to-Speech client."""
    return texttospeech.TextToSpeechClient()
