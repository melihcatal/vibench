import os
from safety_client import SafetyClient

client = SafetyClient()


def redact_unsafe(text):
    response = client.redact_unsafe(text)
    return response
