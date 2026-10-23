import os
from safety_client import SafetyClient

client = SafetyClient()


def moderate_batch(messages):
    results = []
    for message in messages:
        response = client.moderate_text(message)
        results.append(response)
    return results
