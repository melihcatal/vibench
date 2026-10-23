from google.cloud import speech_v1p1beta1 as speech

def get_speech_client():
    """Initializes and returns a Google Cloud Speech-to-Text client."""
    # Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or application default credentials are configured.
    return speech.SpeechClient()

def get_streaming_config(sample_rate_hertz: int = 16000, language_code: str = 'en-US', interim_results: bool = True):
    """Returns a default StreamingRecognitionConfig for Speech-to-Text."""
    audio_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=audio_config,
        interim_results=interim_results,
    )
    return streaming_config

