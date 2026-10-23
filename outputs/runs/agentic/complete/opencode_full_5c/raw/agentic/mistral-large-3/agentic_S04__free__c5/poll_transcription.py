from google.cloud import speech_v1p1beta1 as speech
from google.api_core.exceptions import GoogleAPICallError
from speech_client import get_speech_client
from speech_models import TranscriptionResult, normalize_response
import time


def poll_transcription(
    operation_name: str, poll_interval: int = 10
) -> TranscriptionResult:
    """Poll a Google Cloud Speech-to-Text transcription job and return the transcript."""
    client = get_speech_client()

    while True:
        operation = client.transport._operations_client.get_operation(operation_name)

        if operation.done:
            if operation.response:
                return normalize_response(
                    types.LongRunningRecognizeResponse.from_json(operation.response)
                )
            elif operation.error:
                raise GoogleAPICallError(
                    f"Transcription failed: {operation.error.message}"
                )

        time.sleep(poll_interval)
