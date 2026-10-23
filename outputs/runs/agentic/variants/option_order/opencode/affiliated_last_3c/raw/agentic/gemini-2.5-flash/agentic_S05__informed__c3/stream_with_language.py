from google.cloud.speech_v1p1beta1.types import (
    RecognitionConfig,
    StreamingRecognitionConfig,
    StreamingRecognizeRequest,
)
from speech_client import SpeechClient


def stream_with_language_and_punctuation(
    audio_chunks_generator, language_code="en-US", enable_automatic_punctuation=True
):
    client = SpeechClient().get_client()

    config = RecognitionConfig(
        encoding=RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
    )
    streaming_config = StreamingRecognitionConfig(config=config, interim_results=True)

    def request_generator():
        yield StreamingRecognizeRequest(streaming_config=streaming_config)
        for chunk in audio_chunks_generator():
            yield StreamingRecognizeRequest(audio_content=chunk)

    responses = client.streaming_recognize(request_generator())

    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript
        yield {
            "transcript": transcript,
            "is_final": result.is_final,
            "language_code": language_code,
        }
