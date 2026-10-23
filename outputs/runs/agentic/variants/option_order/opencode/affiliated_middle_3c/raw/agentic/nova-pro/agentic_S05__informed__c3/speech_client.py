import dashscope

from dashscope import AudioAsync


def get_speech_client():
    return dashscope.AudioAsync


def get_streaming_config(language="en-US"):
    return dashscope.AudioAsync.StreamingConfig(language=language)
