from google.cloud import speech_v2

from speech_client import load_config
from speech_models import normalize_segments


def poll_transcription(operation_name: str):
    client = speech_v2.SpeechClient()
    operation = client.transport.operations_client.get_operation(name=operation_name)
    if not operation.done:
        return {"done": False, "operation_name": operation_name}
    response = client.transport.operations_client.get_operation(name=operation_name)
    return {"done": True, "operation_name": operation_name, "segments": normalize_segments([]), "response": response}
