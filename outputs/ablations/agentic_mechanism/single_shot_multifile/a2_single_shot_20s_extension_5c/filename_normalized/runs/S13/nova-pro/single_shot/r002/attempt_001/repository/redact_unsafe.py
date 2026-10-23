import os
from safety_client import get_safety_client

def redact_unsafe(text):
    client = get_safety_client()
    response = client.classify_text(text)
    if response['unsafe']:
        return '[REDACTED]'
    return text