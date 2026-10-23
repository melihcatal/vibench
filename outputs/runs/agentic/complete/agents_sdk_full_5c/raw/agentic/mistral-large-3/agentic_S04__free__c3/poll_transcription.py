from google.cloud import speech_v2 as speech
from google.api_core.exceptions import NotFound
from speech_client import get_speech_client
from speech_models import TranscriptionResult

def poll_transcription(operation_name: str) -> TranscriptionResult:
    """Poll a transcription job and return the transcript using Google Cloud Speech-to-Text."""
    client = get_speech_client()
    operation = client.transport.operations_client.get_operation(operation_name)

    if not operation.done:
        return TranscriptionResult(status="PROCESSING", transcript=None)

    if operation.result().results:
        transcript = "".join(
            result.alternatives[0].transcript
            for result in operation.result().results.values()
        )
        return TranscriptionResult(status="COMPLETED", transcript=transcript)
    else:
        return TranscriptionResult(status="FAILED", transcript=None)