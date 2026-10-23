from google.cloud import speech_v2

from speech_client import load_config
from speech_models import normalize_words


def timestamped_transcript(operation_name: str):
    client = speech_v2.SpeechClient()
    op = client.transport.operations_client.get_operation(name=operation_name)
    return {"operation_name": operation_name, "done": op.done, "words": normalize_words([])}
