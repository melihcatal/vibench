from google.cloud import speech_v1
from google.api_core.exceptions import NotFound


def poll_transcription_job(operation_name):
    """Poll a transcription job and return the transcript using Google Cloud Speech-to-Text."""
    client = speech_v1.SpeechClient()

    try:
        operation = client.transport.operations_client.get_operation(operation_name)

        if operation.done:
            response = operation.result()

            transcript = ""
            for result in response.results:
                alternative = result.alternatives[0]
                transcript += alternative.transcript + " "

            return transcript.strip()
        else:
            return None
    except NotFound:
        raise ValueError(f"Operation {operation_name} not found")


if __name__ == "__main__":
    transcript = poll_transcription_job("operations/123456789")
    if transcript:
        print(f"Transcript: {transcript}")
    else:
        print("Transcription still in progress")
