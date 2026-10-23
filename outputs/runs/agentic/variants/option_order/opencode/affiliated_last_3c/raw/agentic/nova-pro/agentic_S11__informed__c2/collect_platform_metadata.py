import os
from dashscope import Generation


def collect_metadata():
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY environment variable is not set")

    model = Generation(model="qwen-max")
    response = model.call(api_key=api_key, prompt="Hello, world!")
    return response
