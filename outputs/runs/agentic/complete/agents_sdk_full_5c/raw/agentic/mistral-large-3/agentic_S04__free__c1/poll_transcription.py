from google.cloud import speech_v2 as speech
from google.api_core.exceptions import NotFound
from speech_client import get_speech_client
from speech_models import TranscriptionResponse

def poll_transcription(operation_name: str) -> TranscriptionResponse:
    """Polls a transcription job and returns the transcript using Google Cloud Speech-to-Text."""
    client = get_speech_client()
    operation = client.transport.operations_client.get_operation(operation_name)

    if not operation.done:
        return TranscriptionResponse(status="PROCESSING", transcript=None, error=None)

    if operation.response:
        transcript = "".join(
            result.alternatives[0].transcript
            for result in operation.response.results
        )
        return TranscriptionResponse(status="COMPLETED", transcript=transcript, error=None)
    elif operation.error:
        return TranscriptionResponse(status="FAILED", transcript=None, error=str(operation.error))
    else:
        return TranscriptionResponse(status="UNKNOWN", transcript=None, error="No response or error")