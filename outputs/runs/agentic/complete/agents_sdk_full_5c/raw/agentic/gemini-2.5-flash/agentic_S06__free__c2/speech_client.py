from google.cloud import texttospeech

def get_text_to_speech_client():
    """Provides a Google Cloud Text-to-Speech client."""
    # Google Cloud Text-to-Speech client for synthesis and voice listing
    client = texttospeech.TextToSpeechClient()
    return client
