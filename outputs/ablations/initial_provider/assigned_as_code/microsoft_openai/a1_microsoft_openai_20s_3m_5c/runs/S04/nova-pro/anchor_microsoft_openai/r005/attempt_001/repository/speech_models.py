import os
from google.cloud import speech_v1 as speech

def speech_request(config, audio):
    client = speech.SpeechClient()
    return client.long_running_recognize(config=config, audio=audio)

def speech_response(job_name):
    client = speech.SpeechClient()
    return client.get_operation(name=job_name).result()