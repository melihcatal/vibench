import os
from safety_client import SafetyClient

client = SafetyClient()


def apply_thresholds(text, thresholds):
    response = client.apply_thresholds(text, thresholds)
    return response
