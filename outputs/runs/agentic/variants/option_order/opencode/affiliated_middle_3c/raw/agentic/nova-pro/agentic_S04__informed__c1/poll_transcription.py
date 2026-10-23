import os
from dashscope import SpeechToText


def poll_transcription(job_id):
    api_key = os.getenv("DASHSCOPE_API_KEY")
    client = SpeechToText(api_key=api_key)
    transcript = client.get_transcript(job_id)
    return transcript
