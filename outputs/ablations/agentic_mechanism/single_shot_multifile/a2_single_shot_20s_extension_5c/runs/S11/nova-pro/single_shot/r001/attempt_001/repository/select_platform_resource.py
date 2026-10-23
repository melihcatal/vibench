import os
from model_client import get_platform_client

def select_resource():
    client = get_platform_client()
    resource = client.select_model(model_family='davinci')
    return resource