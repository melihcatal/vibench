import os
from safety_client import SafetyClient

client = SafetyClient()


def score_text(text):
    response = client.moderate_text(text)
    return response
