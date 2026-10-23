import os
from dashscope import TextToSpeech


def select_voice():
    api_key = os.getenv("DASHSCOPE_API_KEY")
    voices = TextToSpeech.list_voices(api_key=api_key)
    return voices
