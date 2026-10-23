import re

def check_secret_labels(secret_labels):
    unsafe_patterns = [r'password', r'secret', r'key']
    for label in secret_labels:
        for pattern in unsafe_patterns:
            if re.search(pattern, label, re.IGNORECASE):
                return False
    return True