import dashscope

from dashscope import AudioAsync


def partial_results():
    config = dashscope.AudioAsync.StreamingConfig()
    with AudioAsync.stream(config) as stream:
        for result in stream:
            if result.is_final:
                print("Final result:", result.transcript)
            else:
                print("Interim result:", result.transcript)
