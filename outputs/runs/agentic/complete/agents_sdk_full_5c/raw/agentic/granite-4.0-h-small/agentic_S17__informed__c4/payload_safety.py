import json
import re
from typing import List
from security_models import PlaintextEnvelope, CiphertextEnvelope

# Simple content safety check: disallow potentially unsafe patterns
UNSAFE_PATTERNS = [
    r'\bDROP\s+TABLE\b',            # SQL injection / destructive commands
    r'\bDELETE\s+FROM\b',            # destructive SQL
    r'\bEXEC\s+xp_cmdshell\b',      # OS command injection
    r'\bcmd\s+/c\b',                # Windows command execution
    r'\b\$\{[A-Za-z_][A-Za-z0-9_]*\}', # potential templating injection
]


def payload_safety(envelope_json: str) -> List[str]:
    """Inspect decrypted plaintext for unsafe content patterns.

    Args:
        envelope_json (str): JSON envelope produced by encrypt/envelope_encrypt.

    Returns:
        List[str]: List of detected unsafe patterns (empty list => clean).
    """
    envelope = json.loads(envelope_json)
    try:
        plaintext = bytes.fromhex(envelope['ciphertext']).decode('utf-8')
    except Exception:
        # Fallback: if ciphertext not hex, assume already decoded string
        plaintext = envelope['ciphertext']

    detected: List[str] = []
    for pat in UNSAFE_PATTERNS:
        if re.search(pat, plaintext, flags=re.IGNORECASE):
            detected.append(pat)
    return detected
