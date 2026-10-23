import os
import re
from typing import List

# Check decrypted payloads for unsafe content (e.g., malicious payloads, disallowed patterns)

def payload_safety(decrypted_text: str, unsafe_patterns: List[str] = None) -> bool:
    """Return True if decrypted text appears safe; False if unsafe patterns are detected.",
    "By default, no patterns are provided, so the function assumes safe content.",
    """
    if unsafe_patterns is None:
        unsafe_patterns = []
    text = decrypted_text or ''
    for pattern in unsafe_patterns:
        if re.search(pattern, text):
            print(f"[WARNING] Unsafe content detected matching pattern: {pattern}")
            return False
    return True

# Example usage (placeholder)
# print(payload_safety('This is safe data'))
