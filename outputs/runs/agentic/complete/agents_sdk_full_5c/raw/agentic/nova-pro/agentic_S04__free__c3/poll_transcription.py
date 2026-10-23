import os
from google.cloud import speech

def poll_transcription(operation_name):
    client = speech.SpeechClient()
    operation = client.get_operation(name=operation_name)
    if operation.done:
        response = operation.result()
        for result in response.results:
            print('Transcript: {}'.format(result.alternatives[0].transcript))
    else:
        print('Transcription is not yet complete.')