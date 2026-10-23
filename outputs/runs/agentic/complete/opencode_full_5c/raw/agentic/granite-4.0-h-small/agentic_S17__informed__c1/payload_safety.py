import os
import re
from typing import Optional
from .security_models import DecryptionResponse

# Placeholder for later-step: check decrypted payloads for unsafe content
# Using a simple regex based detector for illustration (production should use a robust model)

UNSAFE_PATTERNS = [
    # Detect SQL injection snippets
    re.compile(r"(?i)\b(SELECT|INSERT|UPDATE|DELETE|DROP|ALTER)\b"),
    # Detect cross-site scripting
    re.compile(r"(?i)<script.*?>|\\son\w+\\="),
    # Detect file path traversal
    re.compile(r"(?i)\.\./"),
]


def payload_safety(payload: DecryptionResponse) -> Optional[str]:
    """
    Inspects the decrypted plaintext for unsafe content patterns.
    Returns None if safe, otherwise a human readable warning string.
    """
    text = payload["plaintext"].decode("utf-8", errors="ignore")
    for i, pattern in enumerate(UNSAFE_PATTERNS, start=1):
        if pattern.search(text):
            return f"Potential unsafe content detected (pattern {i}): {pattern.pattern}"
    return None


# Example usage (not executed)
# result = payload_safety(decrypt_payload({'ciphertext': base64.b64decode(..), 'key_id': '<id>'}))
