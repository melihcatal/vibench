import os
import json
from safety_client import SafetyClient
from safety_models import SafetyModels

def redact_unsafe(text: str) -> str:
    """Flag or redact unsafe spans in a single text using Azure AI Content Safety.
    Returns the original text with unsafe tokens wrapped in \"[UNSAFE]\" tags.
    """
    client = SafetyClient()
    payload = SafetyModels.build_payload(text)
    raw = client.detect(text)
    normalized = SafetyModels.normalize_response(raw)
    flags = normalized.get('flags', [])
    for flag in flags:
        start, end = flag['start'], flag['end']
        text = text[:start] + "[UNSAFE]" + text[end:]
    return text

if __name__ == "__main__":
    sample = "This includes a bad word."
    print(redact_unsafe(sample))
