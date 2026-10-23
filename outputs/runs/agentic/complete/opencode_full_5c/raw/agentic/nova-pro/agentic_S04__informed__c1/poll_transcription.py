import os
from dashscope import AudioAsync


def poll_transcription(job_id):
    api_key = os.getenv("DASHSCOPE_API_KEY")
    client = AudioAsync(api_key=api_key)
    transcript = client.get_result(job_id)
    return transcript
