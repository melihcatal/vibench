from google.cloud import speech

def get_speech_client():
    """Returns a Google Cloud Speech-to-Text client."""
    return speech.SpeechClient()
