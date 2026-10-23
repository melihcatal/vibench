from google.cloud import speech_v1p1beta1 as speech
from speech_client import get_speech_client, get_streaming_config
from speech_models import TranscriptionResult


def process_streaming_events(responses):
    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript
        is_final = result.is_final
        yield TranscriptionResult(transcript, is_final)
