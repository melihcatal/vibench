from __future__ import annotations

from security_client import SecurityClient

# Google Cloud Natural Language safety review for decrypted payloads.

def payload_safety(payload: str):
    client = SecurityClient()
    return client.review_payload_safety(payload)
