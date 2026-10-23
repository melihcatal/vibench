import os
from speech_client import SpeechClient

client = SpeechClient()

def get_diarized_transcript(audio_file_path):
    job = client.submit_diarization_job(audio_file_path)
    job_id = job['id']
    result = client.poll_diarization_job(job_id)
    return result['diarized_transcript']