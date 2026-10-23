import os
from dashscope import AudioAsync


def diarized_transcript(audio_file_path):
    api_key = os.getenv("DASHSCOPE_API_KEY")
    client = AudioAsync(api_key=api_key)
    job = client.submit(audio_file_path, diarization=True)
    return job.job_id
