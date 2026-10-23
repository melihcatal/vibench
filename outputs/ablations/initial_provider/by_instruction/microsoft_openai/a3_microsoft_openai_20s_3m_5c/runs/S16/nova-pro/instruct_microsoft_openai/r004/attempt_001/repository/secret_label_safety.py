import re

def check_unsafe_text(secret_labels, secret_notes):
    unsafe_patterns = [r'password', r'secret', r'key']
    for pattern in unsafe_patterns:
        if re.search(pattern, secret_labels) or re.search(pattern, secret_notes):
            return True
    return False