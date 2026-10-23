import os
from speech_client import SpeechClient

client = SpeechClient()

def diarized_transcript(file_path):
    response = client.diarized_transcript(file_path)
    return response['diarized_transcript']