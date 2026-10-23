from __future__ import annotations

from security_client import SecurityClient

# Google Cloud Translation API integration.

def compliance_note_translate(text: str, target_language: str = "en"):
    client = SecurityClient()
    return client.translate_compliance_note(text, target_language=target_language)
