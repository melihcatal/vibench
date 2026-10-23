import os
from dashscope import TextToSpeech


def get_speech_client():
    api_key = os.getenv("DASHSCOPE_API_KEY")
    return TextToSpeech(api_key=api_key)
