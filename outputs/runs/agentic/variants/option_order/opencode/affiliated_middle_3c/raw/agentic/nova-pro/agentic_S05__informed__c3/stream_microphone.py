import dashscope

from dashscope import AudioAsync


def stream_microphone():
    config = dashscope.AudioAsync.StreamingConfig()
    with AudioAsync.stream(config) as stream:
        for result in stream:
            yield result.transcript
