import os
from dashscope import SpeechToText


def diarized_transcript(audio_file_path):
    api_key = os.getenv("DASHSCOPE_API_KEY")
    client = SpeechToText(api_key=api_key)
    job = client.submit_job(audio_file_path, diarization=True)
    return job.id
