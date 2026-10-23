import os
from [HELPER] safety_client import get_safety_client

client = get_safety_client()

def redact_unsafe(text):
    response = client.text_moderation.redact(text=text)
    return response.redacted_text