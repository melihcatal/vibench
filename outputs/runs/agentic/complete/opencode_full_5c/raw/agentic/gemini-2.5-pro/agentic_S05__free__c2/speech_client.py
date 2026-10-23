from google.cloud import speech


def get_speech_client():
    """Initializes and returns a Google Cloud Speech-to-Text client."""
    return speech.SpeechClient()


def get_async_speech_client():
    """Initializes and returns an async Google Cloud Speech-to-Text client."""
    return speech.SpeechAsyncClient()
