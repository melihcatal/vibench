from google.cloud import speech_v1p1beta1 as speech
from google.api_core.exceptions import GoogleAPICallError, RetryError
from speech_client import SpeechClient
from speech_models import SpeechNormalizer, TranscriptionResult
import time


def poll_transcription(
    operation_name: str, poll_interval: int = 10, timeout: int = 3600
) -> TranscriptionResult:
    """
    Polls a transcription job and returns the transcript using Google Cloud Speech-to-Text.

    Args:
        operation_name: The operation name returned by submit_transcription.
        poll_interval: Seconds to wait between polls (default: 10).
        timeout: Maximum seconds to wait (default: 3600).

    Returns:
        TranscriptionResult containing the transcript segments.
    """
    client = speech.SpeechClient()
    operation = client.transport._operations_client.get_operation(operation_name)

    start_time = time.time()
    while not operation.done():
        if time.time() - start_time > timeout:
            raise TimeoutError(
                f"Transcription polling timed out after {timeout} seconds."
            )
        time.sleep(poll_interval)
        operation = client.transport._operations_client.get_operation(operation_name)

    if operation.error.message:
        raise GoogleAPICallError(f"Transcription failed: {operation.error.message}")

    response = operation.response
    return SpeechNormalizer.normalize_response(response)
