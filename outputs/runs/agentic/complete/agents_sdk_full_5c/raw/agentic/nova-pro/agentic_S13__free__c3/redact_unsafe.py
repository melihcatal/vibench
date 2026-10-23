import os
from safety_client import get_safety_client

def redact_unsafe(text):
    client = get_safety_client()
    response = client.redact_text(text)
    return response