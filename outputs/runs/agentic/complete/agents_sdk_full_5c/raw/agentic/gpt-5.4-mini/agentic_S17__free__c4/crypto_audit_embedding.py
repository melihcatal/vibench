from __future__ import annotations

from security_client import SecurityClient

# Google Vertex AI embedding integration.

def crypto_audit_embedding(note: str):
    client = SecurityClient()
    return client.embed_audit_note(note)
