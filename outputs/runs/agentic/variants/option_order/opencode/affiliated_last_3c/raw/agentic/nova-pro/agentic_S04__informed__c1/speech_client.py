import os


def get_client():
    api_key = os.getenv("DASHSCOPE_API_KEY")
    from dashscope import ASR

    return ASR(api_key=api_key)
