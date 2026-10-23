from google.cloud import speech_v1p1beta1 as speech


def start_streaming_recognizer(
    sample_rate_hertz: int,
    language_code: str = "en-US",
    enable_automatic_punctuation: bool = True,
):
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        model="video",
        enable_automatic_punctuation=enable_automatic_punctuation,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    return client, streaming_config
