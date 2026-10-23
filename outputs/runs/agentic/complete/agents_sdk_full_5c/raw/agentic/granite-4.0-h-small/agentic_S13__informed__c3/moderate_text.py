import os
import json
from safety_client import SafetyClient
from safety_models import SafetyModels

def moderate_text(user_text: str) -> dict:
    """Score a single text for unsafe or policy‑violating content using Azure AI Content Safety.
    Returns a dict with the provider's raw response and a simple safety decision.
    """
    client = SafetyClient()
    payload = SafetyModels.build_payload(user_text)
    raw = client.detect(user_text)  # wrapper around requests.post(...)
    normalized = SafetyModels.normalize_response(raw)
    return {
        "provider": "Azure",
        "raw": raw,
        "normalized": normalized,
        "is_safe": normalized['result'] == "safe"
    }

if __name__ == "__main__":
    print(moderate_text("This is a test message."))
