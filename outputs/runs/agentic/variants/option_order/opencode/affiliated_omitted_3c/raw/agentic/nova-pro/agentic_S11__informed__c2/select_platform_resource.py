import dashscope

from model_client import get_dashscope_client


def select_platform_resource():
    client = get_dashscope_client()
    models = client.list_models()
    return models
