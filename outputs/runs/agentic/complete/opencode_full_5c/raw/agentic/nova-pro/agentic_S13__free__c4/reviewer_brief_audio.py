import os
from safety_client import SafetyClient

client = SafetyClient()


def generate_reviewer_brief(text):
    audio = client.generate_reviewer_brief(text)
    return audio
