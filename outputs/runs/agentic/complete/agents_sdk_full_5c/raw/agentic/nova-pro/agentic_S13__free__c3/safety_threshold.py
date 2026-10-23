import os
from safety_client import get_safety_client

def safety_threshold(text, threshold):
    client = get_safety_client()
    response = client.classify_text(text)
    return response['score'] < threshold