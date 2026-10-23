from typing import Optional
from google.cloud import texttospeech

def get_speech_client(
    credentials_path: Optional[str] = None
) -> texttospeech.TextToSpeechClient:
    """
    Initializes and returns a Google Cloud Text-to-Speech client.
    
    Authentication is handled by the environment variable GOOGLE_APPLICATION_CREDENTIALS.
    """
    if credentials_path:
        return texttospeech.TextToSpeechClient.from_service_account_file(credentials_path)
    return texttospeech.TextToSpeechClient()
