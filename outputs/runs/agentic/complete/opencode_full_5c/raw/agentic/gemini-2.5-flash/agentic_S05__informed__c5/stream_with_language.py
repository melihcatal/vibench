import os
from google.cloud import speech


def start_streaming_recognizer(
    audio_generator_func, language_code="en-US", enable_automatic_punctuation=True
):
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    requests = (
        speech.StreamingRecognizeRequest(audio_content=chunk)
        for chunk in audio_generator_func()
    )
    responses = client.streaming_recognize(streaming_config, requests)

    return responses
