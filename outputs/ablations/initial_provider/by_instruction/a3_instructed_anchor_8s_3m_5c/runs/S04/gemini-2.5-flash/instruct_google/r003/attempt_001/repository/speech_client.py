from google.cloud import speech_v1p1beta1

def get_speech_client():
    """Initializes and returns a Google Cloud Speech-to-Text client."""
    return speech_v1p1beta1.SpeechClient()
