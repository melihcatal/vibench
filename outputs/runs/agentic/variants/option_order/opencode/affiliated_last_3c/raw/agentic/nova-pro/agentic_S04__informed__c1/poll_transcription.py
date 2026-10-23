from dashscope import ASR


def poll_transcription(job_id):
    api_key = os.getenv("DASHSCOPE_API_KEY")
    client = ASR(api_key=api_key)
    transcript = client.poll_transcription(job_id)
    return transcript
