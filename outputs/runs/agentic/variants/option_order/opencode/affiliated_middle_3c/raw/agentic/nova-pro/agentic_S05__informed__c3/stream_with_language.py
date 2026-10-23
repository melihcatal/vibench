import dashscope

from dashscope import AudioAsync


def stream_with_language(language="en-US"):
    config = dashscope.AudioAsync.StreamingConfig(language=language)
    with AudioAsync.stream(config) as stream:
        for result in stream:
            yield result.transcript
