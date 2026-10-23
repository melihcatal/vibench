import os
from dashscope import BatchAudioTranscription


def timestamped_transcript(audio_file_path):
    api_key = os.getenv("DASHSCOPE_API_KEY")
    client = BatchAudioTranscription(api_key=api_key)
    job = client.create_job(audio_file_path, timestamps=True)
    return job.job_id
