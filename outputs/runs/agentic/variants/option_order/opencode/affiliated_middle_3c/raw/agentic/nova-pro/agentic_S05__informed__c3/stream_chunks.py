import dashscope

from dashscope import AudioAsync


def stream_chunks():
    config = dashscope.AudioAsync.StreamingConfig()
    with AudioAsync.stream(config) as stream:
        for chunk in stream.chunks:
            yield chunk
