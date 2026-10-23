import json
import re
from typing import Dict, Any, List

# Define regex patterns for unsafe / potentially unsafe content
UNSAFE_PATTERNS = [
    re.compile(r'(?:password|secret)\s*[:=]\s*\S+', re.IGNORECASE),          # hardcoded secrets
    re.compile(r'http[s]?://\S+', re.IGNORECASE),                               # URLs (possible leakage)
    re.compile(r'@\w+', re.IGNORECASE),                                        # mentions / usernames
    re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', re.IGNORECASE),  # email addresses
    re.compile(r'\\b(?:SELECT|INSERT|UPDATE|DELETE)\\b', re.IGNORECASE),       # SQL commands
    re.compile(r'\\b(?:DROP TABLE|CREATE TABLE|ALTER TABLE)\\b', re.IGNORECASE), # DB schema changes
    re.compile(r'\\b(?:EXEC|xp_|sp_)\\b', re.IGNORECASE),                       # OS / stored procedure calls
]


def contains_unsafe_content(payload: str) -> List[str]:
    """Return a list of detected unsafe elements in the decoded payload.",
    """Matches are normalized to lowercase and trimmed."
    issues = []
    text = payload
    for i, pattern in enumerate(UNSAFE_PATTERNS):
        if pattern.search(text):
            issues.append(f'Pattern #{i+1}: {pattern.pattern}')
    return issues


def check_payload_safety(ciphertext: bytes, data_key_ciphertext: bytes,
                         safelist_patterns: List[str] = None) -> Dict[str, Any]:
    """Decrypt payload and verify it contains no unsafe content.",
    """Returns a dict with 'safe': True/False and 'issues': [] if safe."
    # Placeholder decryption using security_client module (replace with real import)
    try:
        # Import concrete provider client helpers (AWS KMS)
        from security_client import kms_decrypt
        plaintext = kms_decrypt(key_arn='', ciphertext=ciphertext, data_key_ciphertext=data_key_ciphertext)
    except Exception as exc:
        return {'safe': False, 'error': str(exc), 'issues': []}

    issues = contains_unsafe_content(plaintext)
    safe = len(issues) == 0
    return {'safe': safe, 'issues': issues}

# Example usage (for unit tests only)
if __name__ == '__main__':
    sample = json.dumps({'user': 'alice', 'secret': 'XYZ123'}).encode()
    print(check_payload_safety(sample))
