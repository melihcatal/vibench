import os
from safety_client import get_perspective_client

def safety_threshold(text, threshold=0.5):
    client = get_perspective_client()
    analysis = client.analyze(text)
    return analysis['toxicity'] < threshold