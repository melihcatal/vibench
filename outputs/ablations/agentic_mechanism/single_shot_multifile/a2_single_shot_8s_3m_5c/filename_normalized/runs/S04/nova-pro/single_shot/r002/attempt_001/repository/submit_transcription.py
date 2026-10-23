import os
from speech_client import SpeechClient

client = SpeechClient()

def submit_transcription(file_path):
    response = client.submit_transcription(file_path)
    return response['job_id']