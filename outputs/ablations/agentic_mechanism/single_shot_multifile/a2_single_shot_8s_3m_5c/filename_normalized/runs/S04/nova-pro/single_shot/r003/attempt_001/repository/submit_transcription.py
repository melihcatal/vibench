import os
from speech_client import SpeechClient

client = SpeechClient()

def submit_transcription(audio_file_path):
    job = client.submit_transcription_job(audio_file_path)
    return job['id']