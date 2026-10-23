import os
from dashscope import SpeechToText


def get_client():
    api_key = os.getenv("DASHSCOPE_API_KEY")
    return SpeechToText(api_key=api_key)
