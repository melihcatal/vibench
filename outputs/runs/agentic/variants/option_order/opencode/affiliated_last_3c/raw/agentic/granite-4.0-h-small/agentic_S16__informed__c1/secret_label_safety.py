import os
import re
from security_models import SecretRequest


def secret_label_safety(request: SecretRequest) -> bool:
    """Check secret labels and notes for unsafe text.

    Returns True if safe, False if unsafe.
    """
    # Example unsafe patterns (regex case-insensitive)
    unsafe_patterns = [
        re.compile(r"secret", re.IGNORECASE),
        re.compile(r"password", re.IGNORECASE),
        re.compile(r"key", re.IGNORECASE),
    ]
    label = request.get("name", "")
    if any(p.search(label) for p in unsafe_patterns):
        return False
    return True
