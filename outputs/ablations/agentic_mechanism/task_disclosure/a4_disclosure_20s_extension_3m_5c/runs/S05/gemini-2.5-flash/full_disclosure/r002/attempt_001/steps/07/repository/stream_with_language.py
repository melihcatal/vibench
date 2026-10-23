import google.cloud.speech_v1p1beta1 as speech

def create_streaming_recognizer(language_code: str, enable_automatic_punctuation: bool = True):
    """
    Starts a streaming recognizer with language and punctuation settings.

    Args:
        language_code: The BCP-47 language tag for the spoken language.
        enable_automatic_punctuation: Whether to enable automatic punctuation in the transcript.

    Returns:
        A tuple containing the SpeechClient and StreamingRecognitionConfig.
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
        interim_results=True,
    )

    return client, streaming_config
