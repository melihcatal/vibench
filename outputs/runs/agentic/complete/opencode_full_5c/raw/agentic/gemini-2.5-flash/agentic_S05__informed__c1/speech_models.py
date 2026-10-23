from google.cloud import speech


def get_streaming_config(
    language_code: str = "en-US", enable_automatic_punctuation: bool = True
):
    """
    Returns a Google Cloud StreamingRecognitionConfig.

    Args:
        language_code (str): The language of the supplied audio. Defaults to "en-US".
        enable_automatic_punctuation (bool): Whether to enable automatic punctuation. Defaults to True.

    Returns:
        speech.StreamingRecognitionConfig: The streaming recognition configuration.
    """
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
    return streaming_config
