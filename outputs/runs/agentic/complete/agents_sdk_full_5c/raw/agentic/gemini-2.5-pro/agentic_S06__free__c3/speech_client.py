from google.cloud import texttospeech

def get_tts_client():
    """
    Initializes and returns a Google Cloud Text-to-Speech client.

    Authentication is handled automatically via Application Default Credentials.
    https://cloud.google.com/docs/authentication/application-default-credentials

    Returns:
        texttospeech.TextToSpeechClient: An authenticated client.
    """
    return texttospeech.TextToSpeechClient()
