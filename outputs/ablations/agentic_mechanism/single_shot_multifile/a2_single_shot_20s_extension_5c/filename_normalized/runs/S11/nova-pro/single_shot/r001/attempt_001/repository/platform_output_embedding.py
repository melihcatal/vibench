import os
from model_client import get_platform_client

def embed_output(output_text):
    client = get_platform_client()
    embedding = client.get_embedding(output_text)
    return embedding