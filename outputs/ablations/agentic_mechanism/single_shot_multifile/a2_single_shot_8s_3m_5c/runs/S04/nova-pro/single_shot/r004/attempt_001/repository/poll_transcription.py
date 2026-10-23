import os
from speech_client import SpeechClient

client = SpeechClient()

def poll_transcription(job_id):
    response = client.poll_transcription(job_id)
    return response['transcript']