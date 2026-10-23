import os
import dashscope


def get_dashscope_client():
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY environment variable not set")
    return dashscope.TextGeneration(api_key=api_key)
