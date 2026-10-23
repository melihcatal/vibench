from google.cloud import speech_v1p1beta1 as speech
import time
import os

def poll_transcription_job(operation_name: str):
    """Polls a transcription job and returns the transcript.

    Args:
        operation_name: The name of the long-running operation returned by the transcription submission.

    Returns:
        The full transcript text if the operation is complete, otherwise None.
    """
    client = speech.SpeechClient()

    operation = client.operations_client.get_operation(name=operation_name)

    if operation.done:
        response = speech.LongRunningRecognizeResponse(operation.response)
        transcript = " ".join([result.alternatives[0].transcript for result in response.results])
        print(f"Transcription complete. Transcript: {transcript}")
        return transcript
    else:
        print("Transcription job is still in progress.")
        return None

if __name__ == '__main__':
    # Example usage (replace with your actual operation name)
    OPERATION_NAME = os.getenv("TRANSCRIPTION_OPERATION_NAME", "projects/your-gcp-project-id/locations/global/operations/your-operation-id")

    if "your-operation-id" in OPERATION_NAME:
        print("Please set the TRANSCRIPTION_OPERATION_NAME environment variable or replace 'your-operation-id' with an actual operation ID.")
    else:
        print(f"Polling operation: {OPERATION_NAME}")
        transcript = None
        while transcript is None:
            transcript = poll_transcription_job(OPERATION_NAME)
            if transcript is None:
                time.sleep(5) # Wait for 5 seconds before polling again
        print("Final Transcript:", transcript)
