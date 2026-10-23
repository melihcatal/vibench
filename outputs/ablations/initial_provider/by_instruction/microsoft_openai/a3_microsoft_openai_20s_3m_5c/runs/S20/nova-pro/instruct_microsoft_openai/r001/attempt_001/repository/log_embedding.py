import os
import json
import requests

from observability_client import ObservabilityClient

def embed_log_message(log_message):
    client = ObservabilityClient()
    embedding = client.embed_message(log_message)
    return embedding

if __name__ == '__main__':
    log_message = 'User logged in successfully'
    result = embed_log_message(log_message)
    print(result)