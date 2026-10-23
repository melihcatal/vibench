from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types
from speech_models import SpeechModels, TranscriptionResult


def poll_transcription(operation_name: str) -> TranscriptionResult:
    """Poll a transcription job and return the transcript using Google Cloud Speech-to-Text."""
    client = speech.SpeechClient()

    operation = client.transport._operations_client.get_operation(operation_name)
    if not operation.done:
        raise ValueError("Transcription job is not yet complete.")

    response = types.LongRunningRecognizeResponse.from_json(operation.response)
    return SpeechModels.normalize_response(response)
