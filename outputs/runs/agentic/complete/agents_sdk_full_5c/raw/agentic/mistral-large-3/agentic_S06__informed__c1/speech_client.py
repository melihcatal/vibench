import os
from google.cloud import texttospeech_v1 as texttospeech
from google.api_core.client_options import ClientOptions

def get_speech_client() -> texttospeech.TextToSpeechClient:
    """
    Initialize and return a Google Cloud Text-to-Speech client.
    """
    client_options = ClientOptions(
        api_endpoint=os.getenv("GOOGLE_TTS_ENDPOINT", "texttospeech.googleapis.com")
    )
    return texttospeech.TextToSpeechClient(
        client_options=client_options
    )