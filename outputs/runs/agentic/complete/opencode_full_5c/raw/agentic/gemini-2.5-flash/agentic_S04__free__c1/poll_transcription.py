import os
from google.cloud import speech_v1p1beta1 as speech
from google.api_core.operation import Operation


def poll_transcription_job(operation_name: str):
    """Polls a transcription job and returns the transcript.

    Args:
        operation_name: The operation name of the long-running transcription job.

    Returns:
        The transcript as a string, or None if the job is not yet complete.
    """
    client = speech.SpeechClient()
    operation = Operation(name=operation_name, client=client)

    if operation.done():
        response = operation.result()
        transcript = ""
        for result in response.results:
            transcript += result.alternatives[0].transcript + " "
        return transcript.strip()
    return None


if __name__ == "__main__":
    # Example usage (replace with an actual operation name)
    operation_name = "projects/your-project-id/locations/global/operations/your-operation-id"  # Replace with a real operation name

    print(f"Polling transcription job: {operation_name}...")
    transcript = poll_transcription_job(operation_name)
    if transcript:
        print("Transcription complete:")
        print(transcript)
    else:
        print("Transcription job not yet complete.")
