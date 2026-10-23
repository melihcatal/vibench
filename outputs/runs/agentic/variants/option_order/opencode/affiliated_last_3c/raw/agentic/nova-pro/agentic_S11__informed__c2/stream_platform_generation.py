import os
from dashscope import Generation


def stream_generation():
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY environment variable is not set")

    model = Generation(model="qwen-max")
    response = model.stream_call(api_key=api_key, prompt="Hello, world!")
    for chunk in response:
        print(chunk)
