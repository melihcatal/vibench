from google.cloud import speech_v1p1beta1 as speech
from google.api_core.operations_v1 import OperationsClient

def poll_transcription(operation_name: str, project_id: str, location: str) -> str:
    client = speech.SpeechClient()
    operations_client = OperationsClient()
    operation = operations_client.get_operation(name=operation_name)
    if operation.done:
        response = client.get_operation(name=operation_name)
        transcript = ''
        for result in response.results:
            transcript += ' '.join([alternative.transcript for alternative in result.alternatives])
        return transcript
    else:
        return 'Transcription not completed'