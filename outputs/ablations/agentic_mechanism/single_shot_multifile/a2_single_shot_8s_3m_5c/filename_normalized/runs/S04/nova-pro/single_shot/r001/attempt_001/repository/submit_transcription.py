import os
from speech_client import SpeechClient

client = SpeechClient()

def submit_transcription(audio_file_path):
    with open(audio_file_path, 'rb') as audio_file:
        response = client.submit_transcription(audio_file)
    return response['jobId']