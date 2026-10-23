import dashscope

from model_client import get_dashscope_client


def invoke_platform_model(input_text):
    client = get_dashscope_client()
    response = client.text_generation(model="qwen-turbo", prompt=input_text)
    return response
