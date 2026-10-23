import re

def check_unsafe_text(label):
    unsafe_patterns = [r'password', r'secret', r'key']
    for pattern in unsafe_patterns:
        if re.search(pattern, label, re.IGNORECASE):
            return True
    return False