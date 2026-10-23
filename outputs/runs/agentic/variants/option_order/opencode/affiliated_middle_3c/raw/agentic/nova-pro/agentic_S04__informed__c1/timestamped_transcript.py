import os
from dashscope import SpeechToText


def timestamped_transcript(audio_file_path):
    api_key = os.getenv("DASHSCOPE_API_KEY")
    client = SpeechToText(api_key=api_key)
    job = client.submit_job(audio_file_path, timestamps=True)
    return job.id
