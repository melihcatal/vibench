import re

def check_secret_labels(labels):
    unsafe_patterns = [r'password', r'secret', r'key']
    for pattern in unsafe_patterns:
        if re.search(pattern, labels, re.IGNORECASE):
            return True
    return False