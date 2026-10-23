from google.cloud import speech_v1p1beta1 as speech

def get_speech_client():
    """Returns a Google Cloud Speech-to-Text client."""
    return speech.SpeechClient()

def get_recognition_config(language_code: str = "en-US", enable_automatic_punctuation: bool = True):
    """Returns a RecognitionConfig for streaming."""
    return speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
    )

def get_streaming_config(language_code: str = "en-US", enable_automatic_punctuation: bool = True):
    """Returns a StreamingRecognitionConfig for streaming."""
    config = get_recognition_config(language_code, enable_automatic_punctuation)
    return speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )
