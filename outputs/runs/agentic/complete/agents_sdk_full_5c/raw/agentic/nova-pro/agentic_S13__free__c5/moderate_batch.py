import os
from safety_client import get_perspective_client

def moderate_batch(texts):
    client = get_perspective_client()
    results = [client.analyze(text) for text in texts]
    return results