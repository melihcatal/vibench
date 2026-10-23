import os
from google.cloud import speech_v1 as speech

def poll_transcription(operation_name):
    client = speech.SpeechClient()
    response = client.get_operation(name=operation_name)
    if response.done:
        return response.result()
    else:
        return None