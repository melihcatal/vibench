from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types
from speech_client import SpeechClient
from speech_models import SpeechResponseParser, TranscriptionResult
import time


def poll_transcription(
    operation_name: str, poll_interval: int = 10
) -> TranscriptionResult:
    """Poll a transcription job and return the transcript using Google Cloud Speech-to-Text."""
    client = speech.SpeechClient()
    operation = client.transport._operations_client.get_operation(operation_name)

    while not operation.done:
        time.sleep(poll_interval)
        operation = client.transport._operations_client.get_operation(operation_name)

    if operation.response:
        response = types.LongRunningRecognizeResponse.from_json(operation.response)
        return SpeechResponseParser.parse_transcription_response(response)
    else:
        raise ValueError(f"Transcription failed: {operation.metadata}")
