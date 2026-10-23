import dashscope

from model_client import get_dashscope_client


def stream_platform_generation(input_text):
    client = get_dashscope_client()
    response = client.text_generation(
        model="qwen-turbo", prompt=input_text, stream=True
    )
    for chunk in response:
        yield chunk
