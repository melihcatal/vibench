import os
from model_client import get_platform_client

def stream_generation(input_text):
    client = get_platform_client()
    for response in client.stream_model_output(model_id='text-davinci-003', input_text=input_text):
        yield response