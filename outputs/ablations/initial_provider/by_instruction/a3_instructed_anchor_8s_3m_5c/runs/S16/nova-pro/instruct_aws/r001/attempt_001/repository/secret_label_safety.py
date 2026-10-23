import re

def check_secret_labels(secret_labels):
    unsafe_patterns = [r'password', r'secret']
    for pattern in unsafe_patterns:
        if re.search(pattern, secret_labels, re.IGNORECASE):
            return False
    return True