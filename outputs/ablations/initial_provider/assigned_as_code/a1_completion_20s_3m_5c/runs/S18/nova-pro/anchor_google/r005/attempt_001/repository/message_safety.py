import re

def check_unsafe_content(payload):
    unsafe_patterns = [r'\b(password|secret|key)\b', r'\b(credit card|bank account)\b']
    for pattern in unsafe_patterns:
        if re.search(pattern, payload, re.IGNORECASE):
            return True
    return False