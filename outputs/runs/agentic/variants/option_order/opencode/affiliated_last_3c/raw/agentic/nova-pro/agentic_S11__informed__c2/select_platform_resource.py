import os
from dashscope import Generation


def select_resource():
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY environment variable is not set")

    model = Generation(model="qwen-max")
    return model
