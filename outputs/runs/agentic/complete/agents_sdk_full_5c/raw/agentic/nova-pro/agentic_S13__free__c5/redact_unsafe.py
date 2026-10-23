import os
from safety_client import get_perspective_client

def redact_unsafe(text):
    client = get_perspective_client()
    analysis = client.analyze(text)
    if analysis['toxicity'] > 0.5:
        return '[REDACTED]'
    return text