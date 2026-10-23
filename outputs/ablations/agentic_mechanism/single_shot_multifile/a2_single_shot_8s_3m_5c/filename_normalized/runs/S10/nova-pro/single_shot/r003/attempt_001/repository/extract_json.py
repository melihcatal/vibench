import os
from model_client import get_hosted_llm_client

client = get_hosted_llm_client()

def extract_json(text):
    response = client.extract_json(text)
    return response['json']