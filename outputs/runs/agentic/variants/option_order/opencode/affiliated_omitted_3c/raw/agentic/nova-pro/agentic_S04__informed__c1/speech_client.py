import os
from dashscope import BatchAudioTranscription


def get_client():
    api_key = os.getenv("DASHSCOPE_API_KEY")
    return BatchAudioTranscription(api_key=api_key)
