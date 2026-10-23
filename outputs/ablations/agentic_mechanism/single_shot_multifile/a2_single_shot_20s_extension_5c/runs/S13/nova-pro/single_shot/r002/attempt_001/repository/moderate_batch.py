import os
from safety_client import get_safety_client

def moderate_batch(texts):
    client = get_safety_client()
    results = [client.classify_text(text) for text in texts]
    return results