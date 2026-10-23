import os
from safety_client import SafetyClient

client = SafetyClient()


def summarize_moderation(decisions):
    summary = client.summarize_moderation(decisions)
    return summary
