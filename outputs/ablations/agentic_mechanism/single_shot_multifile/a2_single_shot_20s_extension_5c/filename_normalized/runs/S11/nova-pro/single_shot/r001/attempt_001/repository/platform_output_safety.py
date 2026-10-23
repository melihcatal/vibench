import os
from model_client import get_platform_client

def check_safety(output_text):
    client = get_platform_client()
    safety_check = client.check_safety(output_text)
    return safety_check