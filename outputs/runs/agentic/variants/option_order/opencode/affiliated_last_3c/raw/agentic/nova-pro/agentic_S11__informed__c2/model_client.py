import os
from dashscope import Generation


def get_client():
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY environment variable is not set")
    return Generation(api_key=api_key)


def get_model():
    return "qwen-max"
