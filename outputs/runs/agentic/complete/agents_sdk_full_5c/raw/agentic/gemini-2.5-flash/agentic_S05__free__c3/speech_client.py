from google.cloud import speech_v1p1beta1 as speech

def get_speech_client():
    """Provides a configured Google Cloud Speech-to-Text client."""
    # Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    return speech.SpeechAsyncClient()
