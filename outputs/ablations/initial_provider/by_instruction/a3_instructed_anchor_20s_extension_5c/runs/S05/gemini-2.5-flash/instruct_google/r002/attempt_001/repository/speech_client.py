from google.cloud import speech_v1p1beta1 as speech


def get_speech_client():
    return speech.SpeechClient()


def create_recognition_config(
    sample_rate_hertz: int,
    language_code: str,
    model: str = "video",
    enable_automatic_punctuation: bool = True,
):
    return speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        model=model,
        enable_automatic_punctuation=enable_automatic_punctuation,
    )


def create_streaming_config(recognition_config, interim_results: bool = True):
    return speech.StreamingRecognitionConfig(
        config=recognition_config,
        interim_results=interim_results,
    )
