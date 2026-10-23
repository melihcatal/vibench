from google.cloud import speech_v1p1beta1 as speech


def start_streaming_recognizer(
    sampling_rate: int, language_code: str, enable_punctuation: bool = True
):
    client = speech.SpeechClient()

    audio_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sampling_rate,
        language_code=language_code,
        enable_automatic_punctuation=enable_punctuation,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=audio_config,
        interim_results=True,
    )
    return client, streaming_config
