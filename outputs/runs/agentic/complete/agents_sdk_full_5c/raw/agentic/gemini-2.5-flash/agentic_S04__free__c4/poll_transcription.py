from google.cloud import speech_v1p1beta1
from speech_client import get_speech_client
import time

def poll_transcription_job(operation_name: str, timeout_seconds: int = 600):
    """
    Polls a Google Cloud Speech-to-Text transcription job and returns the transcript.

    Args:
        operation_name: The name of the long-running operation to poll.
        timeout_seconds: The maximum time to wait for the operation to complete.

    Returns:
        The transcription result as a string, or None if the operation times out or fails.
    """
    client = get_speech_client()

    print(f"Polling operation: {operation_name}")
    start_time = time.time()

    while time.time() - start_time < timeout_seconds:
        operation = client.transport.operations_client.get_operation(operation_name)

        if operation.done:
            if operation.error:
                print(f"Operation failed with error: {operation.error}")
                return None
            else:
                result = speech_v1p1beta1.types.LongRunningRecognizeResponse(operation.response)
                full_transcript = " ".join([alt.transcript for result_obj in result.results for alt in result_obj.alternatives])
                return full_transcript
        else:
            print("Operation not yet done, waiting...")
            time.sleep(10) # Wait for 10 seconds before polling again

    print(f"Operation timed out after {timeout_seconds} seconds.")
    return None
