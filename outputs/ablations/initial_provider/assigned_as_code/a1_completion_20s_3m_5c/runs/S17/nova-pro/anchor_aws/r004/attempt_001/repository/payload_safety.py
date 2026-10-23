import re


def payload_safety(plaintext):
    unsafe_patterns = [
        r'\b(password|secret|token)\b',
        r'\b(credit card|social security number)\b'
    ]
    for pattern in unsafe_patterns:
        if re.search(pattern, plaintext, re.IGNORECASE):
            return False
    return True