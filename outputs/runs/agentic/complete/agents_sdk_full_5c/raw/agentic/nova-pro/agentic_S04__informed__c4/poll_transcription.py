import os
from google.cloud import speech_v1 as speech

def poll_transcription(operation_name):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/credentials.json'
    client = speech.SpeechClient()
    response = client.get_operation(name=operation_name)
    if response.done:
        result = client.operations_client.get_operation(name=operation_name)
        transcript = result.result().results[0].alternatives[0].transcript
        return transcript
    else:
        return 'Transcription not completed'