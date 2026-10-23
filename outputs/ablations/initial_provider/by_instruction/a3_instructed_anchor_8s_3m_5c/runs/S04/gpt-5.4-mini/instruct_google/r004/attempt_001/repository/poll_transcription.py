from google.cloud import speech_v1p1beta1 as speech

from speech_client import get_speech_client
from speech_models import normalize_transcript_text


def poll_transcription(operation_name: str) -> str:
    client = get_speech_client()
    operation = client.transport.operations_client.get_operation(name=operation_name)
    if not operation.done:
        return ""
    result = client.transport.operations_client._get_operation_response(operation_name)
    return normalize_transcript_text(result)
