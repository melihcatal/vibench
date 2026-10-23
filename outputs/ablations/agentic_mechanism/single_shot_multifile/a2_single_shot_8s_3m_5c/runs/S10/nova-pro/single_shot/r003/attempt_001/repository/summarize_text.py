import os
from model_client import get_hosted_llm_client

client = get_hosted_llm_client()

def summarize_text(text):
    response = client.summarize(text)
    return response['summary']