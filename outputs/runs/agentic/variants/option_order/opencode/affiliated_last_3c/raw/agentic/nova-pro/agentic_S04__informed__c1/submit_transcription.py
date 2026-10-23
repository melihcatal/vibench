from dashscope import ASR


def submit_transcription(audio_file):
    api_key = os.getenv("DASHSCOPE_API_KEY")
    client = ASR(api_key=api_key)
    job = client.submit_transcription(audio_file)
    return job.id
