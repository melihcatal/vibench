import speech_client


def stream_with_language(language_code="en-US", enable_automatic_punctuation=True):
    client = speech_client.get_speech_client()
    config = speech_models.create_streaming_config(
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
    )
    streaming_recognizer = client.streaming_recognize(config)
    return streaming_recognizer
