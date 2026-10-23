from google.api_core.operation import Operation
from speech_client import get_operation_client
import time

def poll_transcription_job(operation_name: str, timeout_seconds: int = 600) -> str:
    """Polls a transcription job and returns the complete transcript.

    Args:
        operation_name: The name of the long-running operation returned by the submission.
        timeout_seconds: Maximum time to wait for the operation to complete.

    Returns:
        The concatenated transcript text.

    Raises:
        Exception: If the operation fails or times out.
    """
    client = get_operation_client()
    operation = Operation(operation_name, client)

    print(f"Polling transcription job: {operation_name}...")
    try:
        # Blocks until the operation is complete or timeout is reached
        response = operation.result(timeout=timeout_seconds)

        transcript_parts = []
        for result in response.results:
            # The first alternative is usually the most accurate
            if result.alternatives:
                transcript_parts.append(result.alternatives[0].transcript)

        full_transcript = " ".join(transcript_parts)
        print("Transcription job completed.")
        return full_transcript

    except Exception as e:
        print(f"Transcription job failed or timed out: {e}")
        raise

# Example usage (would typically be run from a separate script or main block)
# if __name__ == "__main__":
#     # Replace with an actual operation name from submit_transcription.py
#     # op_name = "projects/YOUR_PROJECT_NUMBER/locations/global/operations/YOUR_OPERATION_ID"
#     # transcript = poll_transcription_job(op_name)
#     # print(f"Full Transcript: {transcript}")
#     pass
