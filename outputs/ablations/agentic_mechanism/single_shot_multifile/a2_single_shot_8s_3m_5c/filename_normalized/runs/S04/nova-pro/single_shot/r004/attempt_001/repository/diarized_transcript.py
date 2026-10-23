import os
from speech_client import SpeechClient

client = SpeechClient()

def diarized_transcript(job_id):
    response = client.diarized_transcript(job_id)
    return response['diarized_transcript']