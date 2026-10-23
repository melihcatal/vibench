import os
from model_client import get_hosted_llm_client

client = get_hosted_llm_client()

def stream_completion(prompt):
    for token in client.stream_completion(prompt):
        yield token