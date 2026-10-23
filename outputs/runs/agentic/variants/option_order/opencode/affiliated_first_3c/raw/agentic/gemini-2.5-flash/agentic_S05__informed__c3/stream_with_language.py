from google.cloud import speech

from speech_client import get_speech_client
from speech_models import StreamingRecognitionConfig


def start_streaming_recognizer(
    audio_chunks: list[bytes], config: StreamingRecognitionConfig
):
    client = get_speech_client()
    streaming_config = speech.StreamingRecognitionConfig(
        config=speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code=config.language_code,
            enable_automatic_punctuation=config.enable_automatic_punctuation,
        ),
        interim_results=True,
    )

    def request_generator():
        for chunk in audio_chunks:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    responses = client.streaming_recognize(streaming_config, request_generator())
    return responses
