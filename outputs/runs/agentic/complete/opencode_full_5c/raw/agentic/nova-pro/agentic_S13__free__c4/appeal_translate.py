import os
from safety_client import SafetyClient

client = SafetyClient()


def translate_appeal(text):
    translation = client.translate_appeal(text)
    return translation
