from google.cloud import speech_v1p1beta1
from google.api_core.operations_v1 import OperationsClient
from google.api_core.client_options import ClientOptions

def poll_transcription_job(operation_name: str):
    """Polls a Google Cloud Speech-to-Text transcription job and returns the transcript.

    Args:
        operation_name: The name of the long-running operation to poll.
    
    Returns:
        The transcribed text if the operation is complete, otherwise None.
    """
    client_options = ClientOptions(api_endpoint="speech.googleapis.com")
    operations_client = OperationsClient(client_options=client_options)

    operation = operations_client.get_operation(name=operation_name)

    if operation.done:
        response = speech_v1p1beta1.LongRunningRecognizeResponse(operation.response)
        transcript_builder = []
        for result in response.results:
            transcript_builder.append(result.alternatives[0].transcript)
        return " ".join(transcript_builder)
    else:
        return None

