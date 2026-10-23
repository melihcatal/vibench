import os
from model_client import get_platform_client

def collect_metadata(input_text):
    client = get_platform_client()
    response = client.invoke_model_with_metadata(model_id='text-davinci-003', input_text=input_text)
    return response