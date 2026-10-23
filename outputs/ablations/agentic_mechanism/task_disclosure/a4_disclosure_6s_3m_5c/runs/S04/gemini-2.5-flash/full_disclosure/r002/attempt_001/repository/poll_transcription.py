import argparse
import time

from google.cloud import speech_v1p1beta1 as speech
from google.api_core.exceptions import GoogleAPIError

def poll_transcription_job(operation_name: str) -> str:
    """Polls a Google Cloud Speech-to-Text long-running operation and returns the transcript."""
    client = speech.SpeechClient()

    print(f"Polling transcription job: {operation_name}")

    try:
        operation = client.get_operation(name=operation_name)
        while not operation.done:
            print("Transcription job is still in progress. Waiting...")
            time.sleep(10)  # Wait for 10 seconds before polling again
            operation = client.get_operation(name=operation_name)

        if operation.error:
            raise GoogleAPIError(f"Transcription job failed: {operation.error}")

        # The result property is only set if the operation is done and successful
        # Accessing `results` directly if `operation.done` is True and no `operation.error`
        # means the operation completed successfully and has a response.
        if operation.response and operation.response.results:
            transcript = ""
            for result in operation.response.results:
                # The first alternative is the most likely one
                transcript += result.alternatives[0].transcript + "\n"
            return transcript.strip()
        else:
            return "No transcription results found."

    except GoogleAPIError as e:
        print(f"An API error occurred: {e}")
        return f"Error: {e}"
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return f"Error: {e}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Polls a Google Cloud Speech-to-Text transcription job and returns the transcript."
    )
    parser.add_argument("operation_name", help="The full name of the long-running operation (e.g., projects/PROJECT_ID/locations/LOCATION/operations/OPERATION_ID)")
    args = parser.parse_args()

    transcript_result = poll_transcription_job(args.operation_name)
    print("\n--- Transcription Result ---")
    print(transcript_result)
