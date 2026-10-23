import os
from dashscope import BatchAudioTranscription


def poll_transcription(job_id):
    api_key = os.getenv("DASHSCOPE_API_KEY")
    client = BatchAudioTranscription(api_key=api_key)
    result = client.get_job_result(job_id)
    return result.transcription
