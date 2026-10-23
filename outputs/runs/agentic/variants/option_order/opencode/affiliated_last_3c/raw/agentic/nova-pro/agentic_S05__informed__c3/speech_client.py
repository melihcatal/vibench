import os
import dashscope

from dashscope import AudioAsync


def get_speech_client():
    dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")
    return AudioAsync()
