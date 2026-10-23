from dashscope import ASR


def diarized_transcript(audio_file):
    api_key = os.getenv("DASHSCOPE_API_KEY")
    client = ASR(api_key=api_key)
    transcript = client.diarized_transcript(audio_file)
    return transcript
