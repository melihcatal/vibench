import os
from dashscope import AudioAsync


def submit_transcription(audio_file_path):
    api_key = os.getenv("DASHSCOPE_API_KEY")
    client = AudioAsync(api_key=api_key)
    job = client.submit(audio_file_path)
    return job.job_id
