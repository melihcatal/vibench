from dashscope import ASR


def timestamped_transcript(transcription_id):
    api_key = os.getenv("DASHSCOPE_API_KEY")
    client = ASR(api_key=api_key)
    timestamps = client.timestamped_transcript(transcription_id)
    return timestamps
