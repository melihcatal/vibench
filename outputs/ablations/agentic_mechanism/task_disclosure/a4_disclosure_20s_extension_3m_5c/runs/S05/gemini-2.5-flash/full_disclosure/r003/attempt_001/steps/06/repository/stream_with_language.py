from google.cloud import speech_v1p1beta1 as speech

def stream_with_language(language_code: str, enable_automatic_punctuation: bool):
    """
    Starts a streaming recognizer with specified language and punctuation settings.
    """
    client = speech.SpeechClient()

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True
    )
    return streaming_config
