from google.cloud import speech_v1 as speech


def create_streaming_config(language_code, enable_automatic_punctuation):
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
    )
    streaming_config = speech.StreamingRecognitionConfig(config=config)
    return streaming_config
