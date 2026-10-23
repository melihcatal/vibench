from google.cloud import speech
from speech_models import TranscriptionResponse

def timestamped_transcript(operation_name):
    client = speech.SpeechClient()
    operation = client.get_operation(name=operation_name)
    if operation.done:
        response = operation.result()
        return TranscriptionResponse(response)
    else:
        return 'Transcription not completed'