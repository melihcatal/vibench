from google.cloud import speech_v1p1beta1 as speech


def get_streaming_config(sampling_rate: int):
    audio_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sampling_rate,
        language_code="en-US",  # Default language
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=audio_config,
        interim_results=True,
    )
    return streaming_config
