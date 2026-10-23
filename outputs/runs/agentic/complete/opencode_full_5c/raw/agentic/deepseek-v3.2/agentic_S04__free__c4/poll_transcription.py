from google.cloud import speech_v1
from speech_client import get_speech_client


def poll_transcription(operation_name):
    """Poll a transcription job and return the transcript using Google Cloud Speech-to-Text."""
    client = get_speech_client()

    operation = client.transport.operations_client.get_operation(operation_name)

    if not operation.done:
        return None

    response = speech_v1.LongRunningRecognizeResponse.deserialize(
        operation.response.value
    )

    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript + " "

    return transcript.strip()
