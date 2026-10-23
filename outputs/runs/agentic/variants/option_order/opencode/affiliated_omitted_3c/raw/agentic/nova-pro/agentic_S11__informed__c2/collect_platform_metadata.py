import dashscope

from model_client import get_dashscope_client


def collect_platform_metadata(input_text):
    client = get_dashscope_client()
    response = client.text_generation(model="qwen-turbo", prompt=input_text)
    metadata = {
        "usage": response.usage,
        "resource_id": response.id,
        "model_handle": response.model,
    }
    return metadata
