from google.cloud.speech_v1p1beta1.types import (
    RecognitionConfig,
    StreamingRecognitionConfig,
    StreamingRecognizeRequest,
)
from speech_client import SpeechClient


def process_recognition_events(responses):
    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript
        if result.is_final:
            print(f"Final transcript: {transcript}")
            yield {"type": "final", "transcript": transcript}
        else:
            print(f"Partial transcript: {transcript}")
            yield {"type": "partial", "transcript": transcript}


def start_recognizer_and_process(audio_chunks_generator):
    client = SpeechClient().get_client()

    config = RecognitionConfig(
        encoding=RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )
    streaming_config = StreamingRecognitionConfig(config=config, interim_results=True)

    def request_generator():
        yield StreamingRecognizeRequest(streaming_config=streaming_config)
        for chunk in audio_chunks_generator():
            yield StreamingRecognizeRequest(audio_content=chunk)

    responses = client.streaming_recognize(request_generator())
    yield from process_recognition_events(responses)
