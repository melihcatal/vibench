from google.cloud import speech_v1
from google.api_core.operation import Operation


def poll_transcription(operation_name):
    """Poll a transcription job and return the transcript."""
    client = speech_v1.SpeechClient()

    operation = Operation.from_gapic(
        operation_name,
        client._transport.operations_client,
        speech_v1.types.LongRunningRecognizeResponse,
        metadata_type=speech_v1.types.LongRunningRecognizeMetadata,
    )

    if not operation.done():
        print(f"Transcription job {operation_name} is still processing...")
        return None

    response = operation.result()

    transcript = ""
    for result in response.results:
        alternative = result.alternatives[0]
        transcript += alternative.transcript + " "

    return transcript.strip()
