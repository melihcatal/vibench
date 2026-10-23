import os
from speech_client import SpeechClient

client = SpeechClient()

def timestamped_transcript(job_id):
    response = client.timestamped_transcript(job_id)
    return response['timestamped_transcript']