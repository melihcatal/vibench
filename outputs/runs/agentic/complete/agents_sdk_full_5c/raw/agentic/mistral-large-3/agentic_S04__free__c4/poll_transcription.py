from google.cloud import speech_v2 as speech
from google.cloud.speech_v2.types import cloud_speech
from speech_client import get_speech_client
from speech_models import TranscriptionResult

def poll_transcription(operation_name: str) -> TranscriptionResult:
    """Poll a transcription job and return the transcript using Google Cloud Speech-to-Text."""
    client = get_speech_client()
    operation = client.transport.operations_client.get_operation(operation_name)

    if not operation.done:
        return TranscriptionResult(status="PROCESSING", transcript=None)

    response = cloud_speech.BatchRecognizeResults.from_json(
        operation.response.value.decode("utf-8"), ignore_unknown_fields=True
    )

    transcript = "".join(
        result.alternatives[0].transcript
        for result in response.results
        if result.alternatives
    )

    return TranscriptionResult(status="COMPLETED", transcript=transcript)