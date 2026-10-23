import re

def check_unsafe_text(text):
    unsafe_patterns = [
        r'\b(unsafe|malicious|harmful)\b',
    ]
    for pattern in unsafe_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False
