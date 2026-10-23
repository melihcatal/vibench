# redact_unsafe.py
"""Flags or redacts unsafe spans from text based on moderation results.
"""
from safety_client import OpenAIContentSafetyClient
def redact_unsafe(text: str) -> str:
    """Redact any spans flagged as unsafe by the safety model.
    This simple implementation replaces flagged spans with asterisks.
    Returns the sanitized text."""
    client = OpenAIContentSafetyClient()
    response = client.moderate([text])
    result = response[0]["results"][0]
    if not result["flagged"]:
        return text
    # For demo purposes we replace the whole text with redacted content.
    return "[REDACTED - unsafe content detected]"
