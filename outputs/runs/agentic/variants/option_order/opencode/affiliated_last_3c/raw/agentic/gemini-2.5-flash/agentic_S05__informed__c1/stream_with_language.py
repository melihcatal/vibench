import os
from google.cloud import speech_v1p1beta1 as speech
from speech_client import get_speech_client
from speech_models import StreamingRecognitionRequest, normalize_response


def stream_with_language_and_punctuation(
    audio_stream_generator, language_code="en-US", enable_automatic_punctuation=True
):
    """Starts a streaming recognizer with language and punctuation settings."""
    client = get_speech_client()

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

    def request_generator():
        for chunk in audio_stream_generator():
            yield StreamingRecognitionRequest(audio_content=chunk).audio_content

    requests = request_generator()
    responses = client.streaming_recognize(streaming_config, requests)

    for response in responses:
        yield normalize_response(response)
