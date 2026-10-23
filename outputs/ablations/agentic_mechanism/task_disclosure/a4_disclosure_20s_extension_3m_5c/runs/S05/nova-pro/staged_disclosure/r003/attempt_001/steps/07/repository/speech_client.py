from google.cloud import speech_v1p1beta1 as speech

def create_speech_client():
    """Creates a client for streaming speech-to-text."""
    client = speech.SpeechClient()
    return client