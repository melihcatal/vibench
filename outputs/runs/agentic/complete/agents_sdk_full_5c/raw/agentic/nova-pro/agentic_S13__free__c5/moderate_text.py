import os
from safety_client import get_perspective_client

def moderate_text(text):
    client = get_perspective_client()
    analysis = client.analyze(text)
    return analysis