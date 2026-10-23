import re

def check_safety(text):
    unsafe_patterns = [
        r'\b(password|secret|confidential)\b',
        r'\b(credit\s+card|bank\s+account)\b',
        r'\b(social\s+security\s+number)\b'
    ]
    for pattern in unsafe_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return False
    return True