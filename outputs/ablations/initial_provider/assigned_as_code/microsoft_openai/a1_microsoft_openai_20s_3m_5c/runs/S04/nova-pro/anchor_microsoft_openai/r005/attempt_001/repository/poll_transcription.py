import os
from google.cloud import speech_v1 as speech

def poll_transcription(job_name):
    client = speech.SpeechClient()
    job = client.get_operation(name=job_name)
    if job.done:
        return client.get_operation(name=job_name).result()
    else:
        return None