from speech_client import get_speech_client
from google.cloud import speech_v1p1beta1 as speech

def poll_transcription(operation_name: str) -> str | None:
    """Polls a Google Cloud Speech-to-Text transcription job and returns the transcript.

    Args:
        operation_name: The name of the long-running operation.

    Returns:
        The transcribed text if the operation is complete, otherwise None.
    """
    client = get_speech_client()
    operation = client.operations.get(name=operation_name)

    if operation.done:
        response = speech.LongRunningRecognizeResponse(operation.result)
        transcript = "".join([result.alternatives[0].transcript for result in response.results])
        return transcript
    return None
